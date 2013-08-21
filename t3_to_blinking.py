# Victor Amin 2013
# 
# T3 file input adapted from PicoQuant Matlab scripts
# variable names retained from there

import sys
import math
import itertools
import numpy as np

#            ms * convert to ns
resolution = 10 * 1e6 # in ns # int( max(arrivals) * 50e-9 / 5e-3 ) # resolution for resolving on/off times

with open(sys.argv[1], 'rb') as fid:
  #
  # ASCII file header
  #
  print >> sys.stderr, "      Identifier: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 16)))
  print >> sys.stderr, "  Format Version: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 6)))
  print >> sys.stderr, "    Creator Name: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 18)))
  print >> sys.stderr, " Creator Version: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 12)))
  print >> sys.stderr, "       File Time: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 18)))
  np.fromfile(fid, np.byte, 2)
  print >> sys.stderr, "         Comment: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 256)))
  #
  # binary file header
  #
  print >> sys.stderr, ""
  print >> sys.stderr, "Number of Curves: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "   Bits / Record: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "Routing Channels: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "Number of Boards: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "    Active Curve: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "Measurement Mode: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "        Sub-Mode: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "       Range No.: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "          Offset: %d ns" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "Acquisition Time: %d ms" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "         Stop At: %d counts" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "Stop on Overflow: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "         Restart: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, " Display Lin/Log: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, " Display Time Axis From: %d ns" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "   Display Time Axis To: %d ns" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "Display Count Axis From: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "  Display Count Axis To: %d" % np.fromfile(fid, np.int32, 1)[0]
  np.fromfile(fid, np.int32, 16) # skip DispCurve stuff
  np.fromfile(fid, np.single, 9) # skip Param stuff
  print >> sys.stderr, "        Repeat Mode: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "    Repeat  / Curve: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "        Repeat Time: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "   Repeat Wait Time: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "        Script Name: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 20)))
  #
  # board specific header
  #
  print >> sys.stderr, ""
  print >> sys.stderr, "Hardware Identifier: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 16)))
  print >> sys.stderr, "   Hardware Version: %s" % "".join(map(chr, np.fromfile(fid, np.byte, 8)))
  print >> sys.stderr, "   HW Serial Number: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "        Syn Divider: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "CFD ZeroCross (Ch0): %4i mV" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "    CFD Discr (Ch0): %4i mV" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "CFD ZeroCross (Ch1): %4i mV" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "    CFD Discr (Ch1): %4i mV" % np.fromfile(fid, np.int32, 1)[0]
  Resolution = np.fromfile(fid, np.single, 1)[0] # for later
  print >> sys.stderr, "         Resolution: %5.6f ns" % Resolution
  np.fromfile(fid, np.int32, 26) # skip router settings
  #
  # T3 mode specific header
  #
  print >> sys.stderr, ""
  print >> sys.stderr, "   External Devices: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "          Reserved1: %d" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "          Reserved2: %d" % np.fromfile(fid, np.int32, 1)[0]
  CntRate0 = np.fromfile(fid, np.int32, 1)[0] # we'll need this later
  print >> sys.stderr, "   Count Rate (Ch0): %d Hz" % CntRate0
  print >> sys.stderr, "   Count Rate (Ch1): %d Hz" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "         Stop After: %d ms" % np.fromfile(fid, np.int32, 1)[0]
  print >> sys.stderr, "        Stop Reason: %d" % np.fromfile(fid, np.int32, 1)[0]
  Records= np.fromfile(fid, np.uint32, 1)[0]
  print >> sys.stderr, "  Number Of Records: %d" % Records
  print >> sys.stderr, "Imaging Header Size: %d" % np.fromfile(fid, np.int32, 1)[0]
  #
  # T3 mode event records
  #
  print >> sys.stderr, ""
  ofltime = cnt_1 = cnt_2 = cnt_3 = cnt_4 = cnt_Ofl = cnt_M = cnt_Err = 0 # counters
  WRAPAROUND = 65536
  syncperiod = 1E9/CntRate0 # in nanoseconds
  print >> sys.stderr, "Sync Rate = %d / second" % CntRate0
  print >> sys.stderr, "Sync Period = %5.4f ns" % syncperiod
  print >> sys.stderr, ""
  
  print >> sys.stderr, "Outputting blinking histogram with a time resolution of %g ms" % (resolution/1e6)
  
  print >> sys.stderr, "\n...done reading headers."
  T3Record = np.fromfile(fid, np.uint32, Records)
  print >> sys.stderr, "...done reading data."
  # done reading file

# calculate values for table
nsync = T3Record & 65535
chan = (T3Record >> 28) & 15
dtime = (T3Record >> 16) & 4095

ofltime = np.cumsum(chan==15) * WRAPAROUND

# calculate arrivals
synctimes = (ofltime + nsync) * syncperiod
arrivals = dtime[chan==1] * Resolution + synctimes[chan==1]

# arrival to time trace
nbins = int( math.ceil(arrivals[-1]/resolution) ) + 1 # number of bins necessary given resolution and last arrival time
bins = [0]
for i in xrange (1, nbins):
  bins.append(i*resolution)
  
(counts, times) = np.histogram(arrivals, bins)

# blinking
threshold = max(counts)/10 # anything below 10% of max is off
onoff = counts > threshold
grouped_onoff = [(k, sum(1 for i in g)) for k,g in itertools.groupby(onoff)] # creates array where consecutive booleans are grouped into (bool, n) pairs, where n is the number of repeats

# meh, loop
ontimes = []
offtimes = []
for (on, seq) in grouped_onoff: # separate state/count pairs into separate lists
  if on:
    ontimes.append(seq * resolution)
  else:
    offtimes.append(seq * resolution)

maxtime = max(ontimes + offtimes) # we'll use same bins for on/off histograms, so make sure both fit
nbins = int( math.ceil(maxtime/resolution) ) + 1 # number of bins for on/off times histograms
bins = [0] # reusing, don't need time trace bins anymore
for i in xrange (1, nbins):
  bins.append(i*resolution)

(onhist, onbins) = np.histogram(ontimes, bins)
(offhist, offbins) = np.histogram(offtimes, bins)

print >> sys.stderr, "...done parsing data.\n"

print >> sys.stderr, "Printing tab-delimited histogram: [bin/s] [oncounts] [offcounts]"
for i in xrange (0, onbins.size-1):
  print "%g\t%i\t%i" % (onbins[i]/1e9, onhist[i], offhist[i])

print >> sys.stderr, "...done printing data.\n"

print >> sys.stderr, "Resolution: %g ms" % (resolution/1000000)
