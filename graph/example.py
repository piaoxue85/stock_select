import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# plt.subplot(221,axisbg = "r")

# plt.show()
# print matplotlib.rc_params()
#
# matplotlib.rcParams["lines.marker"] = "o"
matplotlib.rcParams["lines.color"] = "green"

# matplotlib.rc("lines",color = "red",marker = "x",linewidth=3)
import pylab
# fig = plt.figure()
# pylab.plot([1,2,3])
# fig.canvas.draw()
# pylab.show()
# fig = plt.figure()
# plt.subplot(222)
# plt.subplot(121)
# ax = fig.add_axes([0.1,0.1,0.5,0.5])
# matplotlib.rcParams["pathch.linewidth"] = 22
# plt.show()
fig = plt.figure()
fig.show()
fig.patch.set_color("g")
fig.set_alpha(0.5)
fig.canvas.draw()
print plt.getp(fig)
plt.show()