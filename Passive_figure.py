#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 20:11:04 2022

@author: roxanne
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

def mystyle():
  """
  Create custom plotting style.

  Returns
  -------
  my_style : dict
      Dictionary with matplotlib parameters.

  """
  # color pallette
  style = {
      # Use LaTeX to write all text
      "text.usetex": False,
      "font.family": "DejaVu Sans",
      "font.weight": "bold",
      # Use 16pt font in plots, to match 16pt font in document
      "axes.labelsize": 16,
      "axes.titlesize": 20,
      "font.size": 16,
      # Make the legend/label fonts a little smaller
      "legend.fontsize": 14,
      "xtick.labelsize": 14,
      "ytick.labelsize": 14,
      "axes.linewidth": 2.5,
      "lines.markersize": 10.0,
      "lines.linewidth": 2.5,
      "xtick.major.width": 2.2,
      "ytick.major.width": 2.2,
      "axes.labelweight": "bold",
      "axes.spines.right": False,
      "axes.spines.top": False
  }

  return style


plt.style.use("seaborn-colorblind")
plt.rcParams.update(mystyle())




##load passive results
with open("results_passive_F_1_9.pickle", "rb") as file:
    results_passive = pickle.load(file)

with open('results_passive_F_3.pickle', 'rb') as file:
    results_passive_F3 = pickle.load(file)
#ith open("employee_info.pickle", "rb") as file:
#    loaded_dict = pickle.load(file)

with open('results_passive_F_1.pickle', 'rb') as file:
    results_passive_F1 = pickle.load(file)
#ith open("employee_info.pickle", "rb") as file:
#    loaded_dict = pickle.load(file)

"""
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)


#F1
ax1.plot(results_passive_F1['time'], results_passive_F1['vsoma'])
ax2.plot(results_passive_F1['time'], results_passive_F1['vapic29'], label="F=1")
#F1.9
ax1.plot(results_passive['time'], results_passive['vsoma'], color='black')
ax2.plot(results_passive['time'], results_passive['vapic29'], color='k', label='F=1.9')
#F4

ax1.plot(results_passive_F3['time'], results_passive_F3['vsoma'], color='r')
ax2.plot(results_passive_F3['time'], results_passive_F3['vapic29'], label="F=4",color='r')
#ax1.legend()
ax2.legend()

ax1.set_xlabel=('time (ms)')
ax2.set_xlabel=('time (ms)')
ax1.set_ylabel=('Vm at soma (mV)')
#ax2.set_ylabel=('Vm at dendrite (mV)')
plt.show()

"""



#fig3, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)

"""
results_passive = {}
results_passive['vsoma'] = np.array(vsoma_vec)
results_passive['vdend1'] = np.array(vdend1_vec)
results_passive['vapic15'] = np.array(vapic15_vec)
results_passive['time'] = np.array(t_vec)

"""
###plot passive result with F=1.9 and soma injection
#fig2, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True,figsize=(8, 6))

#ax2.plot(results_passive_d['time'], results_passive_d['vsoma'], color='black', label='soma')
#ax2.plot(results_passive_d['time'], results_passive_d['vapic15'], color='red', label='apical')
#ax1.legend()
#ax2.legend()




plt.figure(figsize=(8, 6))
plt.plot(results_passive_F1['time'], results_passive_F1['vsoma'],color='red', label='F = 1')
plt.plot(results_passive['time'], results_passive['vsoma'], color='black', label='F = 1.9')
plt.plot(results_passive_F3['time'], results_passive_F3['vsoma'], label='F = 4')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.title('Voltage recorded at soma')
plt.legend()
plt.savefig("F_change_pas_soma.png")
plt.show()


plt.figure(figsize=(8, 6))
plt.plot(results_passive_F1['time'], results_passive_F1['vapic29'],color='red', label='F = 1')
plt.plot(results_passive['time'], results_passive['vapic29'], color='black', label='F = 1.9')
plt.plot(results_passive_F3['time'], results_passive_F3['vapic29'], label='F = 4')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.ylim(-87,-70)
plt.title('Voltage recorded at apical dendrite')
plt.legend()
plt.savefig("F_change_pas_apical.png")
plt.show()


###soma v apical
plt.figure(figsize=(8, 6))

plt.plot(results_passive['time'], results_passive['vsoma'],color='k', label='soma')
plt.plot(results_passive['time'], results_passive['vapic29'], color='r', label='apical')

plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.ylim(-87,-78)
plt.title('F = 1.9')
plt.legend()
plt.savefig("F_19_pas_.png")
plt.show()

plt.figure(figsize=(8, 6))

plt.plot(results_passive_F3['time'], results_passive_F3['vsoma'],color='k', label='soma')
plt.plot(results_passive_F3['time'], results_passive_F3['vapic29'], color='r', label='apical')

plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.ylim(-87,-78)
plt.title('F = 4')
plt.legend()
plt.savefig("F_4_pas_.png")
plt.show()



#active
with open('results_active_F_1_9.pickle', 'rb') as file:
    results_active = pickle.load(file)

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
#results_passive_F3['time'], results_passive_F3['vsoma'], color='r')
