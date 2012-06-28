#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

import numpy
import itertools
from loadsums import pca_loadsum
from pylab import figure, xlabel, ylabel, show, legend
from matplotlib.ticker import MultipleLocator, FuncFormatter, FormatStrFormatter
from load_vdaq_conds import data_type, bytes_per_pixel
from get_data import data_name, lenheader, nframesperstim, framewidth, frameheight
nframesperstim = numpy.array(nframesperstim)

stim_start = 20
stim_length = 5

img_range_one = numpy.arange(nframesperstim, nframesperstim * 2)
img_range_zero = numpy.arange(0, nframesperstim)

one_fimg = pca_loadsum(data_name, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
zero_fimg = pca_loadsum(data_name, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
#one_fimg_norm = (one_fimg / numpy.mean(one_fimg[:,0:stim_start]))
#zero_fimg_norm = (zero_fimg / numpy.mean(zero_fimg[:,0:stim_start])) 
one_coll = numpy.mean(one_fimg, 0)
zero_coll = numpy.mean(zero_fimg, 0)
one_coll_norm = one_coll / numpy.mean(one_coll[:stim_start])
zero_coll_norm = zero_coll / numpy.mean(zero_coll[:stim_start])
rel_coll_one = one_coll_norm / zero_coll_norm


fig = figure(facecolor='#eeeeee')
x0=fig.add_subplot(111)
x0.plot(one_coll_norm, 'r', label="C$_1$")
x0.plot(zero_coll_norm, 'k', alpha = 0.7, label="C$_0$")
x0.plot(rel_coll_one, 'r', alpha = 0.21, label="C$_1$/C$_0$")
x0.hlines(y=min(itertools.chain(zero_coll_norm, one_coll_norm, rel_coll_one)), xmin=0, xmax = stim_start, colors = '#96D0FF', label="Baseline")
x0.hlines(y=min(itertools.chain(zero_coll_norm, one_coll_norm, rel_coll_one)), xmin=stim_start, xmax = stim_start+stim_length, colors = '#0F23FF', label="Stimulus")
x0.axhline(y=1, color = 'k', alpha = 0.12)
ylabel('R/R$_{baseline}$', fontsize='12')
xlabel('Time [s]', fontsize='12')
x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
x0.xaxis.set_minor_locator(MultipleLocator(5))
x0.yaxis.set_major_formatter(FormatStrFormatter('%.5f'))
legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=5, mode="expand", borderaxespad=0.)
x0.set_xlim(0, len(one_coll)-1)
#C = result.T[1]
#a = numpy.reshape(C,(height,height))
#cx1 = x0.imshow(a, interpolation='bilinear', origin='upper', extent=None)
#cbar = fig.colorbar(cx1)
#cbar.set_label('Reflectance change')
#cbar.ax.tick_params(direction='out')

show()
#bpath = os.path.splitext(data_name)[0]
#filecount = len(data_name)
#newname = bpath + '-raw_array.npy'
#numpy.save(newname, one_fimg_pca)