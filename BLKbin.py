#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import struct
import numpy
import os

factor = 4 # which factor to shrink by (cell size = factor*factor) 
endsize = 0 #overrides factor, 0 in order to disable and keep above factor
multiple = True # whether to bin multiple files into one  
from get_data import data_names_get
data_names = data_names_get()


if multiple == True: # code for binning multiple files
    for i in data_names:
        with open(i) as f:
            f.seek(3*4)
            lenheader = struct.unpack('<l', f.read(4))
            f.seek(7*4)
            datatype = struct.unpack('<l', f.read(4))
            f.seek(9*4)
            framewidth = struct.unpack('<l', f.read(4)) #x
            frameheight = struct.unpack('<l', f.read(4)) #y
            nframesperstim = struct.unpack('<l', f.read(4))
            nstimuli = struct.unpack('<l', f.read(4))
            f.seek(0)
            leheader = f.read(1716)
            f.close()        
        if numpy.array(datatype) == 13:
            data_type = '<u4'
            bytes_per_pixel = 4
        elif numpy.array(datatype) == 14:
            data_type = 2
            bytes_per_pixel = 4       
        Nbig = numpy.floor(framewidth)
        if endsize == 0: pass
        else: factor = Nbig / endsize
        Nsmall = numpy.floor(Nbig / factor)
        assert Nsmall == Nbig/factor # ensure "framewidth" is divisible by "factor"
        frames_tot = numpy.arange(0, numpy.array(nstimuli) * numpy.array(nframesperstim))
        frame_size = numpy.floor(framewidth) * numpy.floor(frameheight)
        if i == data_names[0]: #define frameimg variable as blank matrix (but only for the first data_names item run)
            frameimg = numpy.zeros(frame_size*len(frames_tot))
        else: pass
        with open(i) as f:
            f.seek(lenheader[0])
            frameimg_new = numpy.fromstring(f.read(frame_size*4*len(frames_tot)),dtype = data_type, count = frame_size*len(frames_tot))
            frameimg = frameimg + frameimg_new
            f.close()
    bin_frame = frameimg / len(data_names) 
    small = bin_frame.reshape([2*numpy.array(nframesperstim), Nsmall, Nbig/Nsmall, Nsmall, Nbig/Nsmall]).mean(4).mean(2)
    framewidth = frameheight = Nsmall
    #<begin making new file name
    le_path, le_file = os.path.split(data_names[0]) #split at last slash
    le_file, le_extension = os.path.splitext(le_file) # split at last period
    bpath, _ = os.path.splitext(data_names[-1]); lnumber = bpath[bpath.rfind('B'):]
    filecount = len(data_names)
    # name of the first file - "B index" of the last file,fl,number of files,bin,cell binning  
    newname = le_path+'/sets_binned/'+le_file+'-'+lnumber+'fl' + str(len(data_names)) + 'bin' + str(factor) + le_extension
    #end>
    if os.path.isdir(le_path+'/sets_binned/'):
        pass
    else: os.mkdir(le_path+'/sets_binned/')

    with open(newname, "w") as n:
        n.write(leheader)
        bin_frame1 = small.astype('<u4')
        bin_frame2 = bin_frame1.tostring()
        n.write(bin_frame2)
        n.seek(9*4)
        framewidth1 = framewidth.astype('<u4')
        framewidth2 = framewidth1.tostring()
        n.write(framewidth2)
        n.write(framewidth2) # width and height although equal have different entries
        n.close()
else: # code for binning cells in single files
    for i in data_names:
        with open(i) as f:
            f.seek(3*4)
            lenheader = struct.unpack('<l', f.read(4))
            f.seek(7*4)
            datatype = struct.unpack('<l', f.read(4))
            f.seek(9*4)
            framewidth = struct.unpack('<l', f.read(4)) #x
            frameheight = struct.unpack('<l', f.read(4)) #y
            nframesperstim = struct.unpack('<l', f.read(4))
            nstimuli = struct.unpack('<l', f.read(4))
            f.seek(0)
            leheader = f.read(1716)
            f.close()        
        if numpy.array(datatype) == 13:
            data_type = '<u4'
            bytes_per_pixel = 4
        elif numpy.array(datatype) == 14:
            data_type = 2
            bytes_per_pixel = 4   
        Nbig = numpy.floor(framewidth)
        if endsize == 0: pass
        else: factor = Nbig / endsize
        Nsmall = numpy.floor(Nbig / factor)
        print i, framewidth, frameheight, lenheader, data_type, bytes_per_pixel, Nbig, Nsmall
        assert Nsmall == Nbig/factor # ensure "framewidth" is divisible by "factor"
        frames_tot = numpy.arange(0, numpy.array(nstimuli) * numpy.array(nframesperstim))
        frame_size = numpy.floor(framewidth) * numpy.floor(frameheight)
        with open(i) as f:
            f.seek(lenheader[0])
            frameimg = numpy.fromstring(f.read(frame_size*4*len(frames_tot)),dtype = data_type, count = frame_size*len(frames_tot))
            f.close()
        small = frameimg.reshape([2*numpy.array(nframesperstim), Nsmall, Nbig/Nsmall, Nsmall, Nbig/Nsmall]).mean(4).mean(2)
        framewidth = frameheight = Nsmall
        #<begin making new file name
        le_path, le_file = os.path.split(i) #split at last slash
        le_file, le_extension = os.path.splitext(le_file) # split at last period
        newname = le_path+'/single_binned/'+le_file+'bin'+str(factor)+le_extension
        if os.path.isdir(le_path+'/single_binned/'):
            pass
        else: os.mkdir(le_path+'/single_binned/')
        #end>
        with open(newname, "w") as n:
            n.write(leheader)
            bin_frame1 = small.astype('<u4')
            bin_frame2 = bin_frame1.tostring()
            n.write(bin_frame2)
            n.seek(9*4)
            framewidth1 = framewidth.astype('<u4')
            framewidth2 = framewidth1.tostring()
            n.write(framewidth2)
            n.write(framewidth2) # width and height although equal have different entries
            n.close()