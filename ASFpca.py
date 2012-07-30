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
pca = mdp.nodes.PCANode()
pca_result = pca(fimg_ca)
print np.shape(pca_result)
pca_time = pca.get_projmatrix()
print np.shape(pca_time)

print np.shape(fimg_ca)
ica = mdp.nodes.CuBICANode(white_comp=10)
ica_result = ica(fimg_ca)
print np.shape(ica_result)
ica_time = ica.get_projmatrix()
print np.shape(ica_time)


#outfile = data_name + "-ica" + str(np.shape(result)) + ".npy"
#np.save(outfile, result)


fig1 = plt.figure(1,(22,10),facecolor='#eeeeee')

x0=fig1.add_subplot(3,2,1)
x0.plot(pca_time[:,0]-np.mean(pca_time[:stim_start,0]), 'c', alpha = 1, label="Component 1")
x0.plot(pca_time[:,1]-np.mean(pca_time[:stim_start,1]), 'm', alpha = 0.9, label="Component 2")
x0.plot(pca_time[:,2]-np.mean(pca_time[:stim_start,2]), 'y', alpha = 0.8, label="Component 3")
x0.plot(pca_time[:,3]-np.mean(pca_time[:stim_start,3]), 'k', alpha = 0.7, label="Component 4")
#x0.plot(result[:,3], 'r', alpha = 0.7, label="Component 3")
#x0.plot(result[:,4], 'g', alpha = 0.7, label="Component 3")
#x0.plot(result[:,3], 'b', alpha = 0.7, label="Component 4")
#x0.plot(result[:,4], 'c', alpha = 0.7, label="Component 5")
#x0.plot(result[:,0] - result[:,1], 'g', alpha = 0.7, label="Component 2/Component 1")
#x0.hlines(y=min(result), xmin=0, xmax = stim_start, colors = '#96D0FF', label="Baseline")
#x0.hlines(y=min(result), xmin=stim_start, xmax = stim_start+stim_length, colors = '#0F23FF', label="Stimulus")
#x0.axhline(y=0, color = 'k', alpha = 0.12)
ylabel('Component Activity', fontsize='12')
xlabel('Time [s]', fontsize='12')
x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
x0.xaxis.set_minor_locator(MultipleLocator(5))
x0.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
legend(bbox_to_anchor=(1.04, 1.25), ncol=4)
#legend(bbox_to_anchor=(0.5, 4.), loc=4, ncol=10, mode="expand", borderaxespad=0.)
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
grid = ImageGrid(fig1, 323,
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
grid = ImageGrid(fig1, 325,
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

x0=fig1.add_subplot(3,2,2)
x0.plot(ica_time[:,0]-np.mean(ica_time[:stim_start,0]), 'c', alpha = 1, label="Component 1")
x0.plot(ica_time[:,1]-np.mean(ica_time[:stim_start,1]), 'm', alpha = 0.9, label="Component 2")
x0.plot(ica_time[:,2]-np.mean(ica_time[:stim_start,2]), 'y', alpha = 0.8, label="Component 3")
x0.plot(ica_time[:,3]-np.mean(ica_time[:stim_start,3]), 'k', alpha = 0.7, label="Component 4")
#x0.plot(result[:,3], 'r', alpha = 0.7, label="Component 3")
#x0.plot(result[:,4], 'g', alpha = 0.7, label="Component 3")
#x0.plot(result[:,3], 'b', alpha = 0.7, label="Component 4")
#x0.plot(result[:,4], 'c', alpha = 0.7, label="Component 5")
#x0.plot(result[:,0] - result[:,1], 'g', alpha = 0.7, label="Component 2/Component 1")
#x0.hlines(y=min(result), xmin=0, xmax = stim_start, colors = '#96D0FF', label="Baseline")
#x0.hlines(y=min(result), xmin=stim_start, xmax = stim_start+stim_length, colors = '#0F23FF', label="Stimulus")
#x0.axhline(y=0, color = 'k', alpha = 0.12)
ylabel('Component Activity', fontsize='12')
xlabel('Time [s]', fontsize='12')
x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
x0.xaxis.set_minor_locator(MultipleLocator(5))
x0.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
legend(bbox_to_anchor=(1.04, 1.25), ncol=4)
x0.set_xlim(0, timepts-1)

C = ica_result[:,0]
height = np.sqrt(len(C))
a0 = np.reshape(C,(height,height))

C = ica_result[:,1]
a1 = np.reshape(C,(height,height))

C = ica_result[:,2]
a2 = np.reshape(C,(height,height))

C = ica_result[:,3]
a3 = np.reshape(C,(height,height))

C = ica_result[:,4]
a4 = np.reshape(C,(height,height))

C = ica_result[:,5]
a5 = np.reshape(C,(height,height))

ZS = [a0, a1, a2]
grid = ImageGrid(fig1, 324,
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
grid = ImageGrid(fig1, 326,
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
show()