#!/usr/bin/env python
import numpy
import matplotlib
matplotlib.use('Agg')
from scipy.cluster.vq import kmeans2, whiten
import pylab
pylab.close()

# generate some random xy points and
# give them some striation so there will be "real" groups.
xy = numpy.random.rand(30,2)
xy[3:8,1] -= .9
xy[22:28,1] += .9
print 

# make some z values
z = numpy.sin(xy[:,1]-0.2*xy[:,1])

# whiten them
z = whiten(z)

# let scipy do its magic (k==3 groups)
res, idx = kmeans2(numpy.array(zip(xy[:,0],xy[:,1],z)),3)

# convert groups to rbg 3-tuples.
colors = ([([0,0,0],[1,0,0],[0,0,1])[i] for i in idx])

# show sizes and colors. each color belongs in diff cluster.
pylab.scatter(xy[:,0],xy[:,1],s=20*z+9, c=colors)
pylab.savefig('/home/chymera/Desktop/clust.png')
print (20*z+9 < 0).any()

#(17:58:21) terrusse: you can also scale the size
#(17:58:23) terrusse: s = s.min()+1.*(s-s.min())/(s.max()-s.min()) or kind of (do not use this with constant array!)
#(17:58:52) terrusse: sorry s =size_mini +1.*(s-s.min())/(s.max()-s.min())