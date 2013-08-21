# Victor Amin 2013
# 
# T3 file input adapted from PicoQuant Matlab scripts
# variable names retained from there

import sys
import math
import numpy as np
import argparse

# parse commandline arguments
parser = argparse.ArgumentParser(
	description="Outputs TSV of a timetrace, in cps vs s.",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("T3", help="you must provide a T3 file as input")
parser.add_argument("-t", "--timetrace-binsize", type=float, default=10, help="choose a binsize for the timetrace, in ms")

args = parser.parse_args()

with open(args.T3, 'rb') as fid:
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
  
  print >> sys.stderr, "Outputting time trace of intensity (in cps vs s) with bin size of %g ms" % args.timetrace_binsize
  
  print >> sys.stderr, "\n...done reading headers."
  T3Record = np.fromfile(fid, np.uint32, Records)
  print >> sys.stderr, "...done reading data."
  # done reading file

# calculate values for table
nsync = T3Record & 65535
chan = (T3Record >> 28) & 15
dtime = (T3Record >> 16) & 4095

ofltime = np.cumsum(chan==15) * WRAPAROUND
synctimes = (ofltime + nsync) * syncperiod
arrivals = dtime[chan==1] * Resolution + synctimes[chan==1]

# compute timetrace
timetrace_binsize = args.timetrace_binsize * 1e6 # convert ms to ns
timetrace_nbinmax = int( math.ceil(arrivals[-1]/timetrace_binsize) ) + 1 # number of bins necessary given bin size and last arrival
timetrace_bins = [0]
for i in xrange (1, timetrace_nbinmax):
	timetrace_bins.append(i*timetrace_binsize)

(timetrace_counts, timetrace_times) = np.histogram(arrivals, timetrace_bins)

print >> sys.stderr, "...done parsing data."

average_count_rate = (sum(timetrace_counts)/(timetrace_binsize*1e-9))/len(timetrace_counts)
print >> sys.stderr, "Average count rate: %g cps" % average_count_rate

for i in xrange (0, timetrace_times.size-1):
  print "%g\t%g" % (timetrace_times[i]/1e9, timetrace_counts[i]/(timetrace_binsize*1e-9))

print >> sys.stderr, "...done printing data.\n"
