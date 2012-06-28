#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

import mdp
import matplotlib.pyplot
import numpy
from loadsums import pca_loadsum
from pylab import figure, xlabel, ylabel, show, title

from load_vdaq_conds import data_type, bytes_per_pixel
from get_data import data_name, lenheader, nframesperstim, framewidth, frameheight
nframesperstim = numpy.array(nframesperstim)

img_range_zero = numpy.arange(0, nframesperstim)
img_range_one = numpy.arange(nframesperstim, nframesperstim * 2)

fimg_pca_one = pca_loadsum(data_name, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_pca_zero = pca_loadsum(data_name, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
fimg_pca = fimg_pca_one / fimg_pca_zero
fimg_pca_norm = (fimg_pca - numpy.mean(fimg_pca)) / numpy.std(fimg_pca)
result = matplotlib.mlab.PCA(fimg_pca).project(fimg_pca)
#result = mdp.pca(fimg_pca)
#result = mdp.fastica(fimg_pca, white_comp=6)
print numpy.shape(result)

fig = figure(facecolor='#eeeeee')

C = result[:,0]
height = numpy.sqrt(len(C))
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,1)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result[:,1]
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,2)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result[:,2]
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,3)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result[:,3]
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,4)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result[:,4]
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,5)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result[:,5]
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,6)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

C = result[:,6]
a = numpy.reshape(C,(height,height))
x0 = fig.add_subplot(3,3,7)
cx0 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
cbar = fig.colorbar(cx0)
cbar.set_label('Reflectance change')
cbar.ax.tick_params(direction='out')

show()