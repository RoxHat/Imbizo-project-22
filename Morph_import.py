from neuron import h,gui

import matplotlib.pyplot as plt
import numpy as np

# helper libraries, included with NEURON
h.load_file("stdlib.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
h.load_file("stdgui.hoc")

#print([x for x in dir(h) if x._contains_('Import')])


# ASC filename
#filename = "200929_mbv3_cell1.ASC"
filename="20180522_MBV02_cell01.ASC"
cell = h.Import3d_Neurolucida3()
# other options check dir(h)
cell.input(filename)

# easiest to instantiate by passing the loaded morphology to the Import3d_GUI
# tool; with a second argument of 0, it won't display the GUI, but it will allow
# use of the GUI's features
i3d = h.Import3d_GUI(cell)
i3d.instantiate(None)

# Make a figure, just for you to see that it works.
ps = h.PlotShape(True)  # False tells h.PlotShape not to use NEURON's gui
ps.plot(plt)
plt.show()

#tools.dist mechanisms.viewers. shape names to see sections
#check out trees tool box

#try apic 2 and apic 29

####################3
#check that I can access sections of the model
for sec in h.allsec():
    print(sec)
soma = h.soma[0]
print(soma.L)
print(dir(soma))

#Check out section lengths and diameters
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