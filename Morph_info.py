#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 11:54:01 2022

@author: roxanne
"""

from neuron import h
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# helper libraries, included with NEURON
h.load_file("stdlib.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
h.load_file("stdgui.hoc")

#print([x for x in dir(h) if x._contains_('Import')])


# ASC filename
filename = "200929_mbv3_cell1.ASC"
cell = h.Import3d_Neurolucida3()
# other options check dir(h)
cell.input(filename)

# easiest to instantiate by passing the loaded morphology to the Import3d_GUI
# tool; with a second argument of 0, it won't display the GUI, but it will allow
# use of the GUI's features
i3d = h.Import3d_GUI(cell, 0)
i3d.instantiate(None)

# Make a figure, just for you to see that it works.
#ps = h.PlotShape(False)  # False tells h.PlotShape not to use NEURON's gui
#ps.plot(plt)
#plt.show()  #uncomment to see plot

#####
#transform into a list of strings and then use.contains to append specific type

#create list of section names as strings
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

# get length of all basals
dend_L = np.zeros(n_dend)
apic_L = np.zeros(n_apic)

dend_diam = np.zeros(n_dend)
apic_diam = np.zeros(n_apic)
for i in range(n_dend):
    dend_L[i]= h.dend[i].L
    dend_diam[i]= h.dend[i].diam
 
for i in range(n_apic):
    apic_L[i]= h.apic[i].L
    apic_diam[i]= h.apic[i].diam
        
    
print(dend_L)
plt.hist(dend_L,bins=10)
plt.ylabel("frequency")
plt.xlabel("Basal dendrite section length um")
plt.show()

fig, ax = plt.subplots()


"""


#check that I can access sections of the model
#for sec in h.allsec():
 #   print(sec)
# soma = h.soma[0]
# print(soma.L)
#print(dir(soma)


"""
