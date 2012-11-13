__author__ = 'Horea Christian'

import numpy
import pyutils.exceptions
from get_data import unpack_block_file

def vdaq_conds(data_name):
    _, nframesperstim, _, _, nstimuli, nvideoframesperdataframe, filesubtype, datatype = unpack_block_file(data_name)
    
    nframes = numpy.array(nframesperstim) * numpy.array(nstimuli)
    r = numpy.arange(1, nframes+1)
    r1 = range(1, 10)
    time_bin = 1000 / numpy.array(nvideoframesperdataframe)
    tim = numpy.arange(1, numpy.array(nframesperstim)+1) * numpy.array(time_bin)
    sumframes = False
    
    if numpy.array(filesubtype) != 11:
        raise pyutils.exceptions.InputError('not a VDAQ file')
    
    if numpy.array(datatype) == 13:
        data_type = '<u4'
        bytes_per_pixel = 4
    elif numpy.array(datatype) == 14:
        data_type = 2
        bytes_per_pixel = 4
    else:
        raise pyutils.exceptions.InputError('Check the data type')
    return data_type, bytes_per_pixel
