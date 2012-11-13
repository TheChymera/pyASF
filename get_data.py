__author__ = 'Horea Christian'

import struct
import gtk


def data_name_get():
    if gtk.pygtk_version < (2,3,90):
        print "PyGtk 2.3.90 or later required for Plot-It"
        raise SystemExit
    dialog = gtk.FileChooserDialog("Choose a block file...",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    
    lefilter = gtk.FileFilter()
    lefilter.set_name("BLK files")
    lefilter.add_pattern("*.BLK")
    lefilter.add_pattern("*.blk")
    dialog.add_filter(lefilter)
    
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        data_name = dialog.get_filename()
        print dialog.get_filename(), 'selected'
    elif response == gtk.RESPONSE_CANCEL:
        print 'Closed, no files selected'
    dialog.destroy()
    return data_name

def data_names_get():
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
    return data_names

def unpack_block_file(blk_file):
    #zfilesize = numpy.fromfile(data_name, '<l', 1)
    #zchecksum_header = numpy.fromfile(data_name, '<l', 30)
    
    with open(blk_file) as f:
        filesize = struct.unpack('<l', f.read(4))
        checksum_header = struct.unpack('<l', f.read(4))
        checksum_data = struct.unpack('<l', f.read(4))
        lenheader = struct.unpack('<l', f.read(4))
        versionid = struct.unpack('<f', f.read(4))
        filetype = struct.unpack('<l', f.read(4))
        filesubtype = struct.unpack('<l', f.read(4))
        datatype = struct.unpack('<l', f.read(4))
        sizeof = struct.unpack('<l', f.read(4))
        framewidth = struct.unpack('<l', f.read(4)) #x
        frameheight = struct.unpack('<l', f.read(4)) #y
        nframesperstim = struct.unpack('<l', f.read(4))
        nstimuli = struct.unpack('<l', f.read(4))
        initialxbinfactor = struct.unpack('<l', f.read(4))
        initialybinfactor = struct.unpack('<l', f.read(4))
        xbinfactor = struct.unpack('<l', f.read(4))
        ybinfactor = struct.unpack('<l', f.read(4))
        username = struct.unpack('<32s', f.read(32))
        recordingdate = struct.unpack('<16s', f.read(16))
        x1roi = struct.unpack('<l', f.read(4))
        y1roi = struct.unpack('<l', f.read(4))
        x2roi = struct.unpack('<l', f.read(4))
        y2roi = struct.unpack('<l', f.read(4))
        # LOCATE DATA AND REF FRAMES 	####################################
        stimoffs = struct.unpack('<l', f.read(4))
        stimsize = struct.unpack('<l', f.read(4))
        frameoffs = struct.unpack('<l', f.read(4))
        framesize = struct.unpack('<l', f.read(4))
        refoffs	 = struct.unpack('<l', f.read(4))
        refsize	 = struct.unpack('<l', f.read(4))
        refwidth = struct.unpack('<l', f.read(4))
        refheight = struct.unpack('<l', f.read(4))
    
        # Common to data files that have undergone some form of
        # "compression" or "summing"
        # i.e. The data in the current file may be the result of
        #      having summed blocks 'a'-'f', frames 1-7
        whichblocks = struct.unpack('<16H', f.read(32))
        whichframes = struct.unpack('<16H', f.read(32))
        
        # DATA ANALYSIS			####################################
        loclip	 = struct.unpack('<l', f.read(4))
        hiclip	 = struct.unpack('<l', f.read(4))
        lopass	 = struct.unpack('<l', f.read(4))
        hipass	 = struct.unpack('<l', f.read(4))
        operationsperformed = struct.unpack('<64s', f.read(64))
    
        # ORA-SPECIFIC			####################################
        magnification = struct.unpack('<f', f.read(4))
        gain = struct.unpack('<H', f.read(2))
        wavelength = struct.unpack('<H', f.read(2))
        exposuretime = struct.unpack('<l', f.read(4))
        nrepetitions = struct.unpack('<l', f.read(4))
        acquisitiondelay = struct.unpack('<l', f.read(4))
        interstiminterval = struct.unpack('<l', f.read(4))
        creationdate = struct.unpack('<16s', f.read(16))
        datafilename = struct.unpack('<64s', f.read(64))
        orareserved = struct.unpack('<256s', f.read(256))
    
    
    
    #======!This part not tested after porting from Octave/Matlab!==================
    #===============================================================================
    # if filesubtype: 13,   #it's dyedaq file
    # 
    #    #  OIHEADER.H
    #    #  last revised 4.5.97 by Chaipi Wijnbergen for DyeDaq
    #    #
    #    #  DyeDaq-specific
    #    includesrefframe =fread(fid,1, 'long');     # 0 or 1
    #    temp =fread(fid,128, 'char');
    #     listofstimuli=temp(1:max(find(temp~=0)))';  # up to first non-zero stimulus
    #    ntrials =fread(fid,1, 'long');
    #    scalefactor =fread(fid,1, 'long');          # bin * trials
    #     cameragain =fread(fid,1, 'short');         # shcameragain        1,   2,   5,  10
    #     ampgain =fread(fid,1, 'short');            # amp gain            1,   4,  10,  16,
    #                                                #                    40,  64, 100, 160,
    #                                               #                    400,1000
    #    samplingrate =fread(fid,1, 'short');       # sampling rate (1/x)
    #                                                #                     1,   2,   4,   8,
    #                                                #                     16,  32,  64, 128,
    #                                                #                     256, 512,1024,2048
    #     average =fread(fid,1, 'short');            # average             1,   2,   4,   8,
    #                                                #                    16,  32,  64, 128
    #     exposuretime =fread(fid,1, 'short');       # exposure time       1,   2,   4,   8,
    #                                                #                    16,  32,  64, 128,
    #                                                #                    256, 512,1024,2048
    #     samplingaverage =fread(fid,1, 'short');    # sampling average    1,   2,   4,   8,
    #                                                #                    16,  32,  64, 128
    #    presentaverage =fread(fid,1, 'short');
    #    framesperstim =fread(fid,1, 'short');
    #    trialsperblock =fread(fid,1, 'short');
    #    sizeofanalogbufferinframes =fread(fid,1, 'short');
    #    cameratrials=fread(fid,1, 'short');
    #    filler = char(fread(fid,106, 'char'))';
    # 
    #    dyedaqreserved =setstr(fread(fid,256, 'char'))';
    #    else   # it's not dyedaq specific
    #===============================================================================
    
        # VDAQ-SPECIFIC			####################################
        includesrefframe		 = struct.unpack('<l', f.read(4))
        listofstimuli = struct.unpack('<256s', f.read(256))
        nvideoframesperdataframe	 = struct.unpack('<l', f.read(4))
        ntrials	 = struct.unpack('<l', f.read(4))
        scalefactor = struct.unpack('<l', f.read(4))
        meanampgain = struct.unpack('<f', f.read(4))
        meanampdc = struct.unpack('<f', f.read(4))
        vdaqreserved = struct.unpack('<256s', f.read(256))
    #end# end of VDAQ specific
    
        # USER-DEFINED			####################################
        user = struct.unpack('<256s', f.read(256))
    
        # COMMENT			####################################
        comment = struct.unpack('<256s', f.read(256))
        #the lenheader variable covers the file up until here, the next value is the first pixel value
        refscalefactor = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor1 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor2 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor3 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor4 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor5 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor6 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        refscalefactor7 = struct.unpack('<l', f.read(4))         # bin * trials for reference
        
    f.close()
    return lenheader, nframesperstim, framewidth, frameheight, nstimuli, nvideoframesperdataframe, filesubtype, datatype
#!!!!!!Starting here: Test stuff!!!!!!######
#print sizeof, exposuretime, nrepetitions, nvideoframesperdataframe, nframesperstim, nstimuli
#print filesize, lenheader, refscalefactor, refscalefactor1, refscalefactor2, refscalefactor3, refscalefactor4, refscalefactor5, refscalefactor6, refscalefactor7
#print nframesperstim, nvideoframesperdataframe