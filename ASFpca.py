#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

from matplotlib.ticker import MultipleLocator, FuncFormatter, FormatStrFormatter
import mdp
import matplotlib.pyplot
import numpy as np
from loadsums import pca_loadsum
from pylab import figure, xlabel, ylabel, show, title, legend

from load_vdaq_conds import data_type, bytes_per_pixel
from get_data import data_name, lenheader, nframesperstim, framewidth, frameheight
nframesperstim = np.array(nframesperstim)

stim_start = 20
stim_length = 5
outfile = data_name + "-pca(80, 8).npy"

timepts = np.array(nframesperstim)
img_range_zero = np.arange(0, nframesperstim)
img_range_one = np.arange(nframesperstim, nframesperstim * 2)

fimg_pca_one = pca_loadsum(data_name, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_pca_zero = pca_loadsum(data_name, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_pca = fimg_pca_one / fimg_pca_zero
#fimg_pca_zero_norm = (fimg_pca_zero - np.mean(fimg_pca_zero)) / np.std(fimg_pca_zero)
#result = matplotlib.mlab.PCA(fimg_pca).project(fimg_pca)
#result = mdp.fastica(fimg_pca, white_comp=6)


inp = fimg_pca.T # where fimg_pca is 120x(504^2)
print np.shape(inp)
pca = mdp.nodes.PCANode(output_dim=1.00, svd=True, reduce=True) # keep only 97% of the input variance
#pca.train(inp)
#pca.stop_training()
result = pca(inp)
print np.shape(result)
print result[0:79,0].ndim
result_img1 = pca.inverse(result[0:79,0])
result_img2 = pca.inverse(result[0:79,1])
result_img3 = pca.inverse(result[0:79,2])
result_img4 = pca.inverse(result[0:79,3])
#result = np.load(outfile)
print np.shape(result[:,0])
print result[:,0]
print np.sqrt(len(result[:,0]))
print np.shape(result[0])
print np.sqrt(len(result[0]))
print np.shape(result_img1)
print result_img1[0], result_img2[0], result_img3[0], result_img1[0]-inp[0]

outfile = data_name + "-pca" + str(np.shape(result)) + ".npy"
np.save(outfile, result)


fig = figure(facecolor='#eeeeee')

x0=fig.add_subplot(3,1,1)
x0.plot(result[:,0], 'k', alpha = 0.12, label="Component 1")
x0.plot(result[:,1], 'r', alpha = 0.7, label="Component 2")
x0.plot(result[:,2], 'g', alpha = 0.7, label="Component 3")
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

C = result_img1[0]
height = np.sqrt(len(C))
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,4)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result_img1[1]
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,5)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result_img1[2]
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,6)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result_img3[0]
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,7)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result_img3[1]
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,8)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result_img3[2]
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,9)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

#C = result[:,6]
#a = np.reshape(C,(height,height))
#x0 = fig.add_subplot(3,3,7)
#cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
#cbar = fig.colorbar(cx0)
#cbar.set_label('Reflectance change')
#cbar.ax.tick_params(direction='out')
#
#C = result[:,7]
#a = np.reshape(C,(height,height))
#x0 = fig.add_subplot(3,3,8)
#cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
#cbar = fig.colorbar(cx0)
#cbar.set_label('Reflectance change')
#cbar.ax.tick_params(direction='out')
#
#C = result[:,8]
#a = np.reshape(C,(height,height))
#x0 = fig.add_subplot(3,3,9)
#cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
#cbar = fig.colorbar(cx0)
#cbar.set_label('Reflectance change')
#cbar.ax.tick_params(direction='out')

show()