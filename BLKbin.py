#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import gtk
import struct
import numpy
import os

if gtk.pygtk_version < (2,3,90):
    print "PyGtk 2.3.90 or later required for Plot-It"
    raise SystemExit
dialog = gtk.FileChooserDialog("Choose a block file...",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
dialog.set_default_response(gtk.RESPONSE_OK)
dialog.set_select_multiple(True)

lefilter = gtk.FileFilter()
lefilter.set_name("BLK files")
lefilter.add_pattern("*.BLK")
lefilter.add_pattern("*.blk")
dialog.add_filter(lefilter)

response = dialog.run()
if response == gtk.RESPONSE_OK:
    data_names = dialog.get_filenames()
    print dialog.get_filename(), 'selected'
elif response == gtk.RESPONSE_CANCEL:
    print 'Closed, no files selected'
dialog.destroy()

with open(data_names[0]) as f:
    f.seek(3*4)
    lenheader = struct.unpack('<l', f.read(4))
    f.seek(7*4)
    datatype = struct.unpack('<l', f.read(4))
    f.seek(9*4)
    framewidth = struct.unpack('<l', f.read(4)) #x
    frameheight = struct.unpack('<l', f.read(4)) #y
    nframesperstim = struct.unpack('<l', f.read(4))
    nstimuli = struct.unpack('<l', f.read(4))
    f.close()
with open(data_names[0]) as f:
    leheader = f.read(1716)
    

if numpy.array(datatype) == 13:
    data_type = '<u4'
    bytes_per_pixel = 4
elif numpy.array(datatype) == 14:
    data_type = 2
    bytes_per_pixel = 4
    
Nbig = numpy.floor(framewidth)
factor = 4 # which factor to shrink by (cell size = factor*factor) 
multiple = False # whether to actually bin multiple files 
Nsmall = numpy.floor(Nbig / factor)
assert Nsmall == Nbig/factor # ensure "framewidth" is divisible by "factor"

frames_tot = numpy.arange(0, numpy.array(nstimuli) * numpy.array(nframesperstim))
frame_size = numpy.floor(framewidth) * numpy.floor(frameheight)
frameimg = numpy.zeros(frame_size*len(frames_tot))

if multiple == True: # code for binning multiple files
    for i in data_names:
        with open(i) as f:
            f.seek(lenheader[0])
            frameimg_new = numpy.fromstring(f.read(frame_size*4*len(frames_tot)),dtype = data_type, count = frame_size*len(frames_tot))
            frameimg = frameimg + frameimg_new
    bin_frame = frameimg / len(data_names) 
    small = bin_frame.reshape([2*numpy.array(nframesperstim), Nsmall, Nbig/Nsmall, Nsmall, Nbig/Nsmall]).mean(4).mean(2)
    framewidth = frameheight = Nsmall
    #<begin make new file name
    bpath, extension = os.path.splitext(data_names[-1]); lnumber = bpath[bpath.rfind('B'):]
    bpath, extension = os.path.splitext(data_names[0]); fnumber = bpath[bpath.rfind('B'):]
    filecount = len(data_names)
    newname = bpath + '-' + lnumber + 'fl' + str(len(data_names)) + 'bin' + str(factor) + extension
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
else: # code for binning cells in single files
    for i in data_names:
        with open(i) as f:
            f.seek(lenheader[0])
            frameimg = numpy.fromstring(f.read(frame_size*4*len(frames_tot)),dtype = data_type, count = frame_size*len(frames_tot))
        small = frameimg.reshape([2*numpy.array(nframesperstim), Nsmall, Nbig/Nsmall, Nsmall, Nbig/Nsmall]).mean(4).mean(2)
        framewidth = frameheight = Nsmall
        #<begin make new file name
        le_path, le_file = os.path.split(i)
        le_file, le_extension = os.path.splitext(le_file)        
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