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
"""
results_passive = {}
results_passive['vsoma'] = np.array(vsoma_vec)
results_passive['vdend1'] = np.array(vdend1_vec)
results_passive['vapic15'] = np.array(vapic15_vec)
results_passive['time'] = np.array(t_vec)

"""

plt.figure(figsize=(8, 6))
plt.plot(results_passive['time'], results_passive['vsoma'], color='black', label='soma')
plt.plot(results_passive['time'], results_passive['vapic15'], color='red', label='apical')
plt.xlabel('time (ms)')
plt.ylabel('mV')
plt.title('Current injection at soma with F= 1.9')
plt.legend()
plt.show()