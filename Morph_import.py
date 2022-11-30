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
#test