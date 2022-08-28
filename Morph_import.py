from neuron import h
import matplotlib.pyplot as plt

# helper libraries, included with NEURON
h.load_file("stdlib.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
h.load_file("stdgui.hoc")


#print([x for x in dir(h) if x._contains_('Import')])
"""
# SWC filename
filename = "ca1_pyramidal.swc"
cell = h.Import3d_SWC_read()
# other options check dir(h)
cell.input(filename)

# easiest to instantiate by passing the loaded morphology to the Import3d_GUI
# tool; with a second argument of 0, it won't display the GUI, but it will allow
# use of the GUI's features
i3d = h.Import3d_GUI(cell, 0)
i3d.instantiate(None)

# Make a figure, just for you to see that it works.
ps = h.PlotShape(False)  # False tells h.PlotShape not to use NEURON's gui
ps.plot(plt)
plt.show()
""" 