#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 11:54:01 2022

@author: roxanne
"""
#update using git in terminal: git init -> git commit -m"commit message"

from neuron import h
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
i3d = h.Import3d_GUI(cell)
i3d.instantiate(None)

# Make a figure, just for you to see that it works.
ps = h.PlotShape(False)  # False tells h.PlotShape not to use NEURON's gui
ps.plot(plt)
plt.show()  #uncomment to see plot

##### ACCESSING MORPHOLOGY SECTIONS#######

#transform into a list of strings and then use.contains to append specific type
strsecs = [str(sec) for sec in h.allsec()]
#print(strsecs)

soma = h.soma[0]
axon = h.axon[0]
apicals=[] # list of apical section names as strings
basals=[]
  
for i in  range(len(strsecs)):    
    if 'dend' in strsecs[i]:
        basals.append(strsecs[i])
    elif 'apic' in strsecs[i]:
        apicals.append(strsecs[i])

        
# get number of apicals and number of basal dendrites
n_dend = len(basals)
n_apic = len(apicals)       

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
CM =1  	# uF/cm2
RM = 21406		# Ohm-cm2		
RA = 281.78	 #Ohm-cm

for sec in h.allsec():
    #sec.insert('pas')
    sec.Ra = RA  # Axial resistance in Ohm * cm
    sec.cm = CM
   # nseg = 1 + 2*int(L/40)
    
"""
  if h.distance(seg)>StepDist:
      seg.cm=CM*F_Spines
      seg.pas.g=(1/RM)*F_Spines
"""

soma.insert('pas')
for seg in soma:
            seg.pas.g = 1/RM # Passive conductance in S/cm2
            seg.pas.e = -65    # Leak reversal potential mV
            
for i in range(n_dend):
    h.dend[i].insert('pas')
    if (h.distance(0, h.dend[i](0))>StepDist): #spine scaling for dendrites further than 60um from soma
        for seg in h.dend[i]:
            seg.cm=CM*F_Spines
            seg.pas.g=(1/RM)*F_Spines
            seg.pas.e = -65
    else:
        h.dend[i].insert('pas')
        for seg in h.dend[i]:
            seg.pas.g = 1/RM # Passive conductance in S/cm2
            seg.pas.e = -65    # Leak reversal potential mV
                
for i in range(n_apic):
    h.apic[i].insert('pas')
    if (h.distance(0, h.apic[i](0))>StepDist):
        for seg in h.apic[i]:
            seg.cm=CM*F_Spines
            seg.pas.g=(1/RM)*F_Spines
            seg.pas.e = -65 
    else:
        for seg in h.apic[i]:
            seg.pas.g = 1/RM # Passive conductance in S/cm2
            seg.pas.e = -65   


###### test pasive channels are working by adding am I clamp stimulus and recording v in a dend

# Simulation parameters
tstop = 1500  # ms
h.dt = 0.1  # ms
vinit = -65  # initial membrane potential



# Add a stimulus at the start of dend1 Section
stim = h.IClamp(h.soma[0](0.5))
stim.delay = 30
stim.dur = 1000
stim.amp = 1

#recording vectors
vsoma_vec = h.Vector().record(h.soma[0](0.5)._ref_v) 
vdend1_vec = h.Vector().record(h.dend[1](0.5)._ref_v) 
vdend5_vec = h.Vector().record(h.dend[5](0.5)._ref_v)   
t_vec = h.Vector().record(h._ref_t)

# reinitialize the simulator and run again
h.finitialize(vinit)
h.continuerun(tstop)

results_passive = {}
results_passive['vsoma'] = np.array(vsoma_vec)
results_passive['vdend1'] = np.array(vdend1_vec)
results_passive['vdend5'] = np.array(vdend5_vec)
results_passive['time'] = np.array(t_vec)

fig2, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
ax1.plot(results_passive['time'], results_passive['vsoma'], label="dend 1")
ax2.plot(results_passive['time'], results_passive['vdend5'], label="dend 5")
ax1.legend()
ax2.legend()



####adding active mechanisms in soma
#compile mod files of not compiled already with nrnivmodl (cd to dir)mechanisms
celsius = 37
NA_BAR = 8000
THA_NA = -43
K_BAR = 3200
EK = -90
AX_NA_BAR = 200
AX_K_BAR = 100
THA_KV = 25

soma.insert('kv') #does not work
soma.insert('na')

tha_na = THA_NA
gbar_na =  NA_BAR
gbar_kv = K_BAR
ek = EK
##specify Rm separately for dendrites vs soma
# Simulation parameters-active
tstop = 1500  # ms
h.dt = 0.1  # ms
vinit = -65  # initial membrane potential



# Add a stimulus at the start of dend1 Section
stim = h.IClamp(h.soma[0](0.5))
stim.delay = 20
stim.dur = 1000
stim.amp = 0.2

#recording vectors
vsoma_vec = h.Vector().record(h.soma[0](0.5)._ref_v) 
vdend1_vec = h.Vector().record(h.dend[1](0.5)._ref_v) 
vdend5_vec = h.Vector().record(h.dend[5](0.5)._ref_v)   
t_vec = h.Vector().record(h._ref_t)

# reinitialize the simulator and run again
h.finitialize(vinit)
h.continuerun(tstop)

results_active = {}
results_active ['vsoma'] = np.array(vsoma_vec)
results_active ['vdend1'] = np.array(vdend1_vec)
results_active ['vdend5'] = np.array(vdend5_vec)
results_active ['time'] = np.array(t_vec)

fig2, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
ax1.plot(results_active['time'], results_active['vsoma'], label="soma")
ax2.plot(results_passive['time'], results_active['vdend5'], label="dend 5")
ax1.legend()
ax2.legend()




#check that I can access sections of the model
#for sec in h.allsec():
 #   print(sec)
# soma = h.soma[0]
# print(soma.L)
#print(dir(soma)



