
#update using git in terminal: git init -> git commit -m"commit message"
#note I have not update passive model parameters to be the same-check
from neuron import h
from neuron.units import mV, ms, um
import matplotlib.pyplot as plt
import numpy as np
import pickle

# helper libraries, included with NEURON
h.load_file("stdlib.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
h.load_file("stdgui.hoc")

# ASC filename
#filename = "200929_mbv3_cell1.ASC"
filename="20180522_MBV02_cell01.ASC"
cell = h.Import3d_Neurolucida3()
cell.input(filename)

# easiest to instantiate by passing the loaded morphology to the Import3d_GUI
# tool; with a second argument of 0, it won't display the GUI, but it will allow
# use of the GUI's features
i3d = h.Import3d_GUI(cell, 0)
i3d.instantiate(None)


##### ACCESSING MORPHOLOGY SECTIONS#######

#transform into a list of strings and then use.contains to append specific type
strsecs = [str(sec) for sec in h.allsec()]

soma = h.soma[0]

apicals=[] # list of apical section names as strings
basals=[]
axon=[]
  
for i in  range(len(strsecs)):    
    if 'dend' in strsecs[i]:
        basals.append(strsecs[i])
    elif 'apic' in strsecs[i]:
        apicals.append(strsecs[i])
    elif 'axon' in strsecs[i]:
         axon.append(strsecs[i])
        
# get number of apicals and number of basal dendrites
n_dend = len(basals)
n_apic = len(apicals)       
n_axon = len(axon)  
# get length and diameter of sections
dend_L = np.zeros(n_dend)
apic_L = np.zeros(n_apic)

dend_diam = np.zeros(n_dend)
apic_diam = np.zeros(n_apic)

####use this for loop for accessing sections####
for i in range(n_dend):
    dend_L[i]= h.dend[i].L
    dend_diam[i]= h.dend[i].diam
 
for i in range(n_apic):
    apic_L[i]= h.apic[i].L
    apic_diam[i]= h.apic[i].diam
        
## Plot Histograms of dendrite properties##
"""
fig1, axes = plt.subplot_mosaic(
    [["basals_L", "basals_d"], ["apicals_L","apicals_d"]]
    )

axes["basals_L"].hist(dend_L,bins=10)
axes["basals_d"].hist(dend_diam,bins=10)
axes["apicals_L"].hist(apic_L,bins=10)
axes["apicals_d"].hist(apic_diam,bins=10)

axes["basals_L"].set_xlabel("Basal section length")
axes["basals_d"].set_xlabel("Basal section diam")
axes["apicals_L"].set_xlabel("Apical section length")
axes["apicals_d"].set_xlabel("Apical section diam")
plt.show()
#!not printing labels properly'
"""

########## insert passive channels #########
##constants##
StepDist = 60 #Almost no spines in human cells within the first 60 um from soma
F_Spines = 1.9       
CM =0.45  	# uF/cm2
RM = 21406		# Ohm-cm2		
RA = 281.78	 #Ohm-cm
EPAS = -86

for sec in h.allsec():
    #sec.insert('pas')
    sec.Ra = RA  # Axial resistance in Ohm * cm
    sec.cm = CM
   # nseg = 1 + 2*int(L/40)


soma.insert('pas')
for seg in soma:
            seg.pas.g = 1/RM # Passive conductance in S/cm2
            seg.pas.e = EPAS    # Leak reversal potential mV
            
for i in range(n_axon):
    h.axon[i].insert('pas')
    for seg in h.axon[i]:
                seg.pas.g = 1/RM # Passive conductance in S/cm2
                seg.pas.e = EPAS 

    for seg in h.axon[i]:
                seg.pas.g = 1/RM # Passive conductance in S/cm2
                seg.pas.e = EPAS             
for i in range(n_dend):
    h.dend[i].insert('pas')
    if (h.distance(0, h.dend[i](0))>StepDist): #spine scaling for dendrites further than 60um from soma
        for seg in h.dend[i]:
            seg.cm=CM*F_Spines
            seg.pas.g=(1/RM)*F_Spines
    else:
        h.dend[i].insert('pas')
        for seg in h.dend[i]:
            seg.pas.g = 1/RM # Passive conductance in S/cm2
            seg.pas.e = EPAS     # Leak reversal potential mV
                
for i in range(n_apic):
    h.apic[i].insert('pas')
    if (h.distance(0, h.apic[i](0))>StepDist):
        for seg in h.apic[i]:
            seg.cm=CM*F_Spines
            seg.pas.g=(1/RM)*F_Spines
    else:
        for seg in h.apic[i]:
            seg.pas.g = 1/RM # Passive conductance in S/cm2
            seg.pas.e = EPAS   


###### test pasive channels are working by adding am I clamp stimulus and recording v in a dend

# Simulation parameters

#h.dt = 0.1  # ms
vinit = EPAS # initial membrane potential



# Add a stimulus 
tstop = 129.06  # ms
stim = h.IClamp(h.soma[0](0.5))
stim.delay = 27.06
stim.dur = 2
stim.amp = 0.2
#h.v_init = EPAS
"""
INJ = 27.06
DUR = 2
TSTOP = 129.06
INJ_AMP = 0.2
nj = h.IClamp(0.5, sec=soma)
inj.amp  = INJ_AMP
inj.dur = DUR
inj.delay = INJ 
h.v_init = E_PAS
h.tstop = TSTOP
"""

#recording vectors
vsoma_vec = h.Vector().record(h.soma[0](0.5)._ref_v) 
vdend1_vec = h.Vector().record(h.dend[1](0.5)._ref_v) 
vapic15_vec = h.Vector().record(h.apic[15](0.5)._ref_v)   
t_vec = h.Vector().record(h._ref_t)


# reinitialize the simulator and run again

#def change_model_pas(CM,RM,RA,StepDist,F_Spines):
h.finitialize(vinit)
h.continuerun(tstop)

results_passive = {}
results_passive['vsoma'] = np.array(vsoma_vec)
results_passive['vdend1'] = np.array(vdend1_vec)
results_passive['vapic15'] = np.array(vapic15_vec)
results_passive['time'] = np.array(t_vec)

with open('results_passive_F_1_9.pickle', 'wb') as file:
    pickle.dump(results_passive , file, protocol=pickle.HIGHEST_PROTOCOL)
#ith open("employee_info.pickle", "rb") as file:
#    loaded_dict = pickle.load(file)


fig2, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
ax1.plot(results_passive['time'], results_passive['vsoma'], label="dend 1")
ax2.plot(results_passive['time'], results_passive['vapic15'], label="dend 5")
ax1.legend()
ax2.legend()



####ADDUNG ACTIVE MECHANISMS####
#compile mod files of not compiled already with nrnivmodl (cd to dir)mechanisms
celsius = 37
NA_BAR = 8000
THA_NA = -43
K_BAR = 3200
EK = -90
AX_NA_BAR = 200
AX_K_BAR = 100
THA_KV = 25

soma.insert('kv') 
soma.insert('na')

for seg in soma:
    seg.na.tha = THA_NA
    seg.na.gbar =  NA_BAR
    seg.kv.gbar = K_BAR
    seg.ek = EK
    
    
for i in range(n_axon):
    h.axon[i].insert('kv')
    h.axon[i].insert('na')
    for seg in h.axon[i]:
        seg.na.tha = THA_NA
        seg.na.gbar =  NA_BAR
        seg.kv.gbar = K_BAR
        seg.ek = EK

##specify Rm separately for dendrites vs soma
# Simulation parameters-active
tstop = 1500  # ms
#h.dt = 0.1  # ms
#vinit = -65  # initial membrane potential



# Add a stimulus at the start of dend1 Section
stim = h.IClamp(h.soma[0](0.5))
stim.delay = 50
stim.dur = 1000
stim.amp = 0.2

#recording vectors
vsoma_vec = h.Vector().record(h.soma[0](0.5)._ref_v) 
vaxon_vec = h.Vector().record(h.axon[-1](0.5)._ref_v) 
vapic15_vec = h.Vector().record(h.apic[15](0.5)._ref_v) 
vdend5_vec = h.Vector().record(h.dend[5](0.5)._ref_v)   
t_vec = h.Vector().record(h._ref_t)

# reinitialize the simulator and run again
h.finitialize(vinit)
h.continuerun(tstop)

results_active = {}
results_active ['vsoma'] = np.array(vsoma_vec)
results_active ['vaxon'] = np.array(vaxon_vec)
results_active ['vapic15'] = np.array(vapic15_vec)
results_active ['vdend5'] = np.array(vdend5_vec)
results_active ['time'] = np.array(t_vec)
with open('results_active_F_1_9.pickle', 'wb') as file:
    pickle.dump(results_active , file, protocol=pickle.HIGHEST_PROTOCOL)

plt.figure(figsize=(8, 6))

plt.plot(results_active['time'], results_active['vsoma'],color='k', label='soma')
#plt.plot(results_passive['time'], results_passive['vapic29'], color='r', label='apical')

plt.xlabel('time (ms)')
plt.ylabel('mV')
#plt.ylim(-87,-78)
plt.title('F = 1.9')
plt.legend()
plt.savefig("F_19_act_.png")
plt.show()
'''
fig3, (ax3, ax4) = plt.subplots(nrows=1, ncols=1)
ax3.plot(results_active['time'], results_active['vsoma'], label="F = 1.9")
#ax4.plot(results_active['time'], results_active['vaxon'], label="axon")
ax3.legend()
a#x4.legend()
'''