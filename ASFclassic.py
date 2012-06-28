#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

import matplotlib.pyplot
import numpy
from loadsums import loadsum
from pylab import figure, xlabel, ylabel, show, title

from load_vdaq_conds import data_type, bytes_per_pixel
from get_data import data_name, lenheader, nframesperstim, framewidth, frameheight


nframesperstim = numpy.array(nframesperstim)
end = nframesperstim
ref_start = 0
ref_stop = 15
cond = 1
img_start = 31
img_stop = end

ref_range = numpy.arange(cond * nframesperstim + ref_start, cond * nframesperstim + ref_stop)
img_range = numpy.arange(cond * nframesperstim + img_start, cond * nframesperstim + img_stop)

#<start making imaged range relative to reference range; division by length(*_range) to obtain median values
fimg_ref = loadsum(data_name, ref_range, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel) / len(ref_range)
fimg_raw = loadsum(data_name, img_range, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel) / len(img_range)
fimg1 = fimg_raw / fimg_ref #normalized to baseline
cond = 0
aref_range = numpy.arange(cond * nframesperstim + ref_start, cond * nframesperstim + ref_stop)
aimg_range = numpy.arange(cond * nframesperstim + img_start, cond * nframesperstim + img_stop)
afimg_ref = loadsum(data_name, aref_range, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel) / len(aref_range)
afimg_raw = loadsum(data_name, aimg_range, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel) / len(aimg_range)
fimg2 = afimg_raw / afimg_ref #normalized to baseline
fimg3 = fimg1 - fimg2 # difference between conditions
fimg = fimg3 / fimg3.mean() / fimg3.std() # normalized and divided by standard deviation
#end>

#<start making point-adjusted divisions for 0.5mm (for a total window size of 4.1mm x 4.1mm), 
xlength_unit = numpy.array(framewidth) / 8.2
ylength_unit = numpy.array(frameheight) / 8.2
#end>

fig = figure(facecolor='#eeeeee')
ax = fig.add_subplot(1,1,1)
cax = ax.imshow(fimg3, interpolation='bilinear', origin='upper', extent=None)
matplotlib.pyplot.tick_params(axis='both', direction='out')
ax.xaxis.set_major_locator(matplotlib.ticker.IndexLocator(xlength_unit, 0))
ax.yaxis.set_major_locator(matplotlib.ticker.IndexLocator(ylength_unit, 0))
ax.set_xticklabels(numpy.linspace(0, 4, 9))
ax.set_yticklabels(numpy.linspace(0, 4, 9))
#ax.xaxis.set_ticks_position("top")
#ax.xaxis.set_label_position("top")

xlabel('Lateral Distance [mm]')
ylabel('Rostral Distance [mm]')
title('Poststimulus [%0.1fs, %0.1fs] values relative to \n Baseline [%0.1fs, %0.1fs] of condition 1 - condition 0' %(img_start / 10, img_stop / 10, ref_start / 10, ref_stop / 10))

cbar = fig.colorbar(cax)
cbar.set_label('Reflectance change')
#cbar.ax.ticklabel_format(style = 'plain')
cbar.ax.tick_params(direction='out')
show()