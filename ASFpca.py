#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

from matplotlib.ticker import MultipleLocator, FuncFormatter, FormatStrFormatter
import mdp
import matplotlib.pyplot as plt
import numpy as np
from loadsums import ca_loadsum
from pylab import figure, xlabel, ylabel, show, title, legend
from mpl_toolkits.axes_grid1 import ImageGrid

from load_vdaq_conds import data_type, bytes_per_pixel
from get_data import data_name, lenheader, nframesperstim, framewidth, frameheight
nframesperstim = np.array(nframesperstim)

stim_start = 20
stim_length = 5

timepts = np.array(nframesperstim)
img_range_zero = np.arange(0, nframesperstim)
img_range_one = np.arange(nframesperstim, nframesperstim * 2)

fimg_ca_one = ca_loadsum(data_name, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_ca_zero = ca_loadsum(data_name, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_ca = fimg_ca_one / fimg_ca_zero 

print np.shape(fimg_ca)
pca = mdp.nodes.PCANode(output_dim=9)
pca_result = pca(fimg_ca)
print np.shape(pca_result)
pca_time = pca.get_projmatrix()
print np.shape(pca_time)
ica_input = pca.inverse(pca_result)
print np.shape(ica_input)
ica = mdp.nodes.CuBICANode(whitened=True)
ica.train(ica_input)
pca_result = ica(ica_input)
pca_time = ica.get_projmatrix()

#outfile = data_name + "-ica" + str(np.shape(result)) + ".npy"
#np.save(outfile, result)


fig = figure(facecolor='#eeeeee')

x0=fig.add_subplot(3,1,1)
x0.plot(pca_time[:,0], 'k', alpha = 0.2, label="Component 1")
x0.plot(pca_time[:,1], 'r', alpha = 0.7, label="Component 2")
x0.plot(pca_time[:,2], 'g', alpha = 0.7, label="Component 3")
x0.plot(pca_time[:,3], 'b', alpha = 0.7, label="Component 3")
x0.plot(pca_time[:,5], 'k', alpha = 1, label="Component 3")
#x0.plot(result[:,3], 'r', alpha = 0.7, label="Component 3")
#x0.plot(result[:,4], 'g', alpha = 0.7, label="Component 3")
#x0.plot(result[:,3], 'b', alpha = 0.7, label="Component 4")
#x0.plot(result[:,4], 'c', alpha = 0.7, label="Component 5")
#x0.plot(result[:,0] - result[:,1], 'g', alpha = 0.7, label="Component 2/Component 1")
#x0.hlines(y=min(result), xmin=0, xmax = stim_start, colors = '#96D0FF', label="Baseline")
#x0.hlines(y=min(result), xmin=stim_start, xmax = stim_start+stim_length, colors = '#0F23FF', label="Stimulus")
#x0.axhline(y=0, color = 'k', alpha = 0.12)
ylabel('R/R$_{baseline}$', fontsize='12')
xlabel('Time [s]', fontsize='12')
x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
x0.xaxis.set_minor_locator(MultipleLocator(5))
x0.yaxis.set_major_formatter(FormatStrFormatter('%.5f'))
legend(bbox_to_anchor=(0., 1.02), loc=3, ncol=5, mode="expand", borderaxespad=0.)
x0.set_xlim(0, timepts-1)

C = pca_result[:,0]
height = np.sqrt(len(C))
a0 = np.reshape(C,(height,height))

C = pca_result[:,1]
a1 = np.reshape(C,(height,height))

C = pca_result[:,2]
a2 = np.reshape(C,(height,height))

C = pca_result[:,3]
a3 = np.reshape(C,(height,height))

C = pca_result[:,4]
a4 = np.reshape(C,(height,height))

C = pca_result[:,5]
a5 = np.reshape(C,(height,height))

ZS = [a0, a1, a2]
grid = ImageGrid(plt.figure(1, (1,1)), 312,
                  nrows_ncols = (1, 3),
                  direction="row",
                  axes_pad = 0.4,
                  cbar_location="top",
                  cbar_mode="each",
                  cbar_size="10%",
                  cbar_pad=0.05
                  )
for ax, z in zip(grid, ZS):
    im = ax.imshow(z,origin="upper",interpolation="none")
    ax.cax.colorbar(im)
    ZS = [a3, a4, a5]
grid = ImageGrid(plt.figure(1, (1,1)), 313,
                  nrows_ncols = (1, 3),
                  direction="row",
                  axes_pad = 0.4,
                  cbar_location="top",
                  cbar_mode="each",
                  cbar_size="10%",
                  cbar_pad=0.05
                  )
for ax, z in zip(grid, ZS):
    im = ax.imshow(z,origin="upper",interpolation="none")
    ax.cax.colorbar(im)

#ZS = [a0, a1, a2]
#grid = ImageGrid(plt.figure(2), 111,
#                  nrows_ncols = (1, 3),
#                  direction="row",
#                  axes_pad = 0.1,
#                  add_all=True,
#                  label_mode = "1",
#                  share_all = True,
#                  cbar_location="right",
#                  cbar_mode="single",
#                  cbar_size="10%",
#                  cbar_pad=0.05
#                  )
#vmax, vmin = np.max(ZS), np.min(ZS)
#import matplotlib.colors
#norm = matplotlib.colors.normalize(vmax=vmax, vmin=vmin)
#
#for ax, z in zip(grid, ZS):
#    im = ax.imshow(z, norm=norm,origin="upper",interpolation="none")
#
## With cbar_mode="single", cax attribute of all axes are identical.
#ax.cax.colorbar(im)
show()