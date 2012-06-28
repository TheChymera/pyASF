__author__ = 'Horea Christian'

import numpy
from get_data import data_name, framewidth, frameheight



def loadsum (filename, frames, sumframes=True, data_type='<u4', xsize=framewidth, ysize=frameheight, lenheader=0, bytes_per_pixel=4):
    
    nframes = len(frames)
    frame_size = numpy.floor(xsize) * numpy.floor(ysize)
    frameimg = numpy.zeros(numpy.floor(xsize)[0], numpy.floor(ysize)[0])
   
    for i in range(0, nframes):
        with open(data_name) as f:
            f.seek(lenheader[0] + frames[i] * bytes_per_pixel * int(frame_size))
            frameimg_new = numpy.fromstring(f.read(frame_size*4),dtype = data_type, count = frame_size).reshape(numpy.floor(xsize), numpy.floor(ysize))
        if sumframes :
            frameimg = frameimg + frameimg_new
        else :
            frameimg = frameimg_new
    return frameimg


def pca_loadsum (filename, frames, sumframes=True, data_type='<u4', xsize=framewidth, ysize=frameheight, lenheader=0, bytes_per_pixel=4):
    
    nframes = len(frames)
    frame_size = numpy.floor(xsize) * numpy.floor(ysize)
    length = numpy.array(xsize) * numpy.array(ysize)
    frameimg = numpy.zeros((length, nframes))
   
    for i in range(0, nframes):
        with open(data_name) as f:
            f.seek(lenheader[0] + frames[i] * bytes_per_pixel * int(frame_size))
            frameimg_new = numpy.fromstring(f.read(frame_size*4),dtype = data_type, count = frame_size)
        if sumframes :
            frameimg[:,i] = frameimg_new  
        else :
            frameimg = frameimg_new
    return frameimg