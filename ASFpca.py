#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

from matplotlib.ticker import MultipleLocator, FuncFormatter, FormatStrFormatter
import mdp
import matplotlib.pyplot
import numpy as np
from loadsums import ca_loadsum
from pylab import figure, xlabel, ylabel, show, title, legend

from load_vdaq_conds import data_type, bytes_per_pixel
from get_data import data_name, lenheader, nframesperstim, framewidth, frameheight
nframesperstim = np.array(nframesperstim)

stim_start = 20
stim_length = 5
outfile = data_name + "-ica(80, 8).npy"

timepts = np.array(nframesperstim)
img_range_zero = np.arange(0, nframesperstim)
img_range_one = np.arange(nframesperstim, nframesperstim * 2)

fimg_ica_one = ca_loadsum(data_name, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_ica_zero = ca_loadsum(data_name, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_ica = fimg_ica_one / fimg_ica_zero
#fimg_ica_zero_norm = (fimg_ica_zero - np.mean(fimg_ica_zero)) / np.std(fimg_ica_zero)
#result = matplotlib.mlab.ica(fimg_ica).project(fimg_ica)
#result = mdp.fastica(fimg_ica, white_comp=6)


inp = fimg_ica.T # where fimg_ica is 120x(504^2)
print np.shape(inp)
ica = mdp.nodes.CuBICANode(white_comp=12)
ica.train(inp)
ica.stop_training()
result = ica(inp)
result_component = np.zeros_like(result) # creates a zeroes matrix of the same shape as "result"
result_component[:,0] = result[:,0] # fills the zeroes matrix with the component of interest
result_img0 = ica.inverse(result_component) # projects component to input space
result_component = np.zeros_like(result) # creates a zeroes matrix of the same shape as "result"
result_component[:,1] = result[:,1] # fills the zeroes matrix with the component of interest
result_img1 = ica.inverse(result_component) # projects component to input space
result_component = np.zeros_like(result) # creates a zeroes matrix of the same shape as "result"
result_component[:,2] = result[:,2] # fills the zeroes matrix with the component of interest
result_img2 = ica.inverse(result_component) # projects component to input space
result_component = np.zeros_like(result) # creates a zeroes matrix of the same shape as "result"
result_component[:,3] = result[:,3] # fills the zeroes matrix with the component of interest
result_img3 = ica.inverse(result_component) # projects component to input space
result_component = np.zeros_like(result) # creates a zeroes matrix of the same shape as "result"
result_component[:,4] = result[:,4] # fills the zeroes matrix with the component of interest
result_img4 = ica.inverse(result_component) # projects component to input space
result_component = np.zeros_like(result) # creates a zeroes matrix of the same shape as "result"
result_component[:,5] = result[:,5] # fills the zeroes matrix with the component of interest
result_img5 = ica.inverse(result_component) # projects component to input space

#result = np.load(outfile)
print np.shape(result[:,0])
print result[:,0]
print np.sqrt(len(result[:,0]))
print np.shape(result[0])
print np.sqrt(len(result[0]))


outfile = data_name + "-ica" + str(np.shape(result)) + ".npy"
np.save(outfile, result)


fig = figure(facecolor='#eeeeee')

x0=fig.add_subplot(3,1,1)
x0.plot(result[:,0], 'r', alpha = 0.7, label="Component 1")
x0.plot(result[:,1], 'k', alpha = 0.2, label="Component 2")
x0.plot(result[:,2], 'g', alpha = 0.7, label="Component 3")
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

C = np.mean(result_img0[stim_start:,], axis=0) / np.mean(result_img0[0:stim_start], axis=0)
height = np.sqrt(len(C))
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,4)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = np.mean(result_img1[stim_start:,], axis=0) / np.mean(result_img1[0:stim_start], axis=0)
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,5)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

#C = result_img2[0] / result[0,2]
C = np.mean(result_img2[stim_start:,], axis=0) / np.mean(result_img2[0:stim_start], axis=0)
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,6)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

#C = result_img2[30] / result[30,2]
C = np.mean(result_img3[stim_start:,], axis=0) / np.mean(result_img3[0:stim_start], axis=0)
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,7)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = np.mean(result_img4[stim_start:,], axis=0) / np.mean(result_img4[0:stim_start], axis=0)
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,8)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = np.mean(result_img5[stim_start:,], axis=0) / np.mean(result_img5[0:stim_start], axis=0)
a = np.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,9)
cx0 = x0.imshow(a, interpolation='none', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

##timcourse0=np.mean(result_img0, 0)
##timcourse1=np.mean(result_img1, 0)
##timcourse2=np.mean(result_img2, 0)
##x0=fig.add_subplot(4,1,4)
##x0.plot(timcourse0 / timcourse0[:stim_start], 'k', alpha = 0.12, label="Component 1")
##x0.plot(timcourse1 / timcourse1[:stim_start], 'r', alpha = 0.7, label="Component 2")
##x0.plot(timcourse2 / timcourse2[:stim_start], 'g', alpha = 0.7, label="Component 3")
#x0=fig.add_subplot(4,1,4)
#x0.plot(np.mean(result_img0, 0), 'k', alpha = 0.12, label="Component 1")
#x0.plot(np.mean(result_img1, 0), 'r', alpha = 0.7, label="Component 2")
#x0.plot(np.mean(result_img2, 0), 'g', alpha = 0.7, label="Component 3")
##x0.plot(result[:,3], 'b', alpha = 0.7, label="Component 4")
##x0.plot(result[:,4], 'c', alpha = 0.7, label="Component 5")
##x0.plot(result[:,0] - result[:,1], 'g', alpha = 0.7, label="Component 2/Component 1")
##x0.hlines(y=min(result), xmin=0, xmax = stim_start, colors = '#96D0FF', label="Baseline")
##x0.hlines(y=min(result), xmin=stim_start, xmax = stim_start+stim_length, colors = '#0F23FF', label="Stimulus")
##x0.axhline(y=0, color = 'k', alpha = 0.12)
#ylabel('R/R$_{baseline}$', fontsize='12')
#xlabel('Time [s]', fontsize='12')
#x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
#x0.xaxis.set_minor_locator(MultipleLocator(5))
#x0.yaxis.set_major_formatter(FormatStrFormatter('%.5f'))
#legend(bbox_to_anchor=(0., 1.02), loc=3, ncol=5, mode="expand", borderaxespad=0.)
#x0.set_xlim(0, timepts-1)

show()