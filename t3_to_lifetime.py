# Victor Amin 2013
# 
# T3 file input adapted from PicoQuant Matlab scripts
# variable names retained from there (even if they're inconsistent)
#
# run with -h or --help for instructions
#

import sys
import math
import numpy as np
import argparse

# parse commandline arguments
parser = argparse.ArgumentParser(
	description="Outputs TSV of an overall lifetime histogram, or in the case that a cutoff is specified, TSV with separate columns for on and off lifetime histograms (columns are [time/ns] [total or on counts] [off counts])",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("T3", help="you must provide a T3 file as input")
parser.add_argument("-l", "--lifetime-binsize-mult", type=int, default=10, help="choose a multiple of the resolution (see header output, typically 0.004-0.016ns) as a bin size for the lifetime histogram(s)")
parser.add_argument("-c", "--cutoff", type=float, default=0, help="choose an intensity cutoff percentage to output separate \"on\" and \"off\" lifetime histograms")
parser.add_argument("-s", "--split", type=int, default=0, help="split into N lifetimes, stratified by bin intensity")
parser.add_argument("-t", "--timetrace-binsize", type=float, default=10, help="choose a binsize for the timetrace, in ms")
parser.add_argument("-z", "--time-zero", type=float, default=0, help="choose a new zero, in ns, to rectify wraparound")

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
	
	print >> sys.stderr, "Outputting lifetime histogram in ns"
	
	print >> sys.stderr, "\n...done reading headers."
	T3Record = np.fromfile(fid, np.uint32, Records)
	print >> sys.stderr, "...done reading data."
	# 
	# done reading file!
	#

# unpack binary values
nsync = T3Record & 65535
chan = (T3Record >> 28) & 15
dtime = (T3Record >> 16) & 4095
# convert dtimes to ns
dtime_shift = np.asarray((dtime[chan==1] * Resolution) - args.time_zero)
dtime_ns = np.where(dtime_shift < 0, abs(dtime_shift) + syncperiod - args.time_zero, dtime_shift)
#dtime_wrap = dtime_shift < 0
#dtime_nowrap = dtime_shift >= 0
#dtime_ns = (dtime_wrap * math.fabs(dtime_shift)) + syncperiod
#dtime_ns = dtime_ns + (dtime_nowrap * dtime_shift)

#dtime_ns = [a*b for a,b in zip(dtime_wrap, dtime_shift)] + syncperiod

# set up lifetime bins
lifetime_binsize = args.lifetime_binsize_mult * Resolution # ns
lifetime_binmax = max(dtime_ns) # ns
lifetime_nbinmax = int( math.ceil(lifetime_binmax / lifetime_binsize) ) + 1

lifetime_bins = [0]
for i in xrange (1, lifetime_nbinmax):
	lifetime_bins.append(i*lifetime_binsize)

# make histograms
if (args.cutoff > 0):
	# if a non-zero cutoff is set, we'll need a timetrace
	# calculate arrivals
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
	timetrace_max = timetrace_counts.max()
	timetrace_min = timetrace_counts.min()

	oncounts_cutoff = timetrace_min + (timetrace_max * (args.cutoff/100))
	offcounts_cutoff = timetrace_min + (timetrace_max * (1-(args.cutoff/100)))
	
	oncounts = timetrace_counts > oncounts_cutoff
	offcounts = timetrace_counts < offcounts_cutoff
	
	j=1 # keep track of what timetrace bin we're in
	oncounts_dtime_ns = []
	offcounts_dtime_ns = []
	for i, arrival in enumerate(arrivals):
		# make sure we're in the right timetrace bin
		if (arrival > timetrace_times[j]):
			j += 1
		# check if this dtime fits in either an on or off bin
		if (oncounts[j-1]):
			oncounts_dtime_ns.append(dtime_ns[i])
		if (offcounts[j-1]):
			offcounts_dtime_ns.append(dtime_ns[i])
	
	(lifetime_oncounts, lifetime_times) = np.histogram(oncounts_dtime_ns, lifetime_bins)
	(lifetime_offcounts, lifetime_times) = np.histogram(offcounts_dtime_ns, lifetime_bins)
	
	print >> sys.stderr, "\nOn cutoff: %i cps\nOff cutoff: %i cps\n" % (oncounts_cutoff/(timetrace_binsize*1e-9), offcounts_cutoff/(timetrace_binsize*1e-9))
	print >> sys.stderr, "Total counts: %i\nOn counts: %i\nOff counts: %i\n" % (len(dtime_ns),len(oncounts_dtime_ns),len(offcounts_dtime_ns))

	for i in xrange (0, lifetime_times.size-1):
		print "%g\t%i\t%i" % (lifetime_times[i], lifetime_oncounts[i], lifetime_offcounts[i])

elif (args.split > 0):
	# if a non-zero split is set, we'll need a timetrace
	# calculate arrivals
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
	timetrace_max = timetrace_counts.max()
	timetrace_min = timetrace_counts.min()
	
	print >> sys.stderr, timetrace_min
	print >> sys.stderr, timetrace_max
	print >> sys.stderr, sum(timetrace_counts)
	
	split_cutoffs = [0 for i in range(args.split+1)]
	split_upper = [[] for i in range(args.split+1)]
	split_lower = [[] for i in range(args.split+1)]

	for i in xrange (1, args.split+1):
		split_cutoffs[i] = timetrace_min + (timetrace_max * (i/float(args.split)))
		split_upper[i] = timetrace_counts <= split_cutoffs[i]
		split_lower[i] = timetrace_counts > split_cutoffs[i-1]
	
	#print "\nCutoffs array:"
	#print split_cutoffs
	
	#print split_upper
	#print split_lower
	j=1 # keep track of what timetrace bin we're in
	split_dtime_ns = [[] for i in range(args.split+1)]
	for i, arrival in enumerate(arrivals):
		# make sure we're in the right timetrace bin
		if (arrival > timetrace_times[j]):
			j += 1
		# check if this dtime fits in a split
		for k in xrange (1, args.split+1):
			if (split_upper[k][j-1] and split_lower[k][j-1]):
				split_dtime_ns[k].append(dtime_ns[i])
				break

	
	lifetime_counts = [[] for i in range(args.split+1)]
	lifetime_times = [[] for i in range(args.split+1)]
	for i in xrange (1, args.split+1):
		(lifetime_counts[i], lifetime_times[i]) = np.histogram(split_dtime_ns[i], lifetime_bins)
	
#	print >> sys.stderr, "\nOn cutoff: %i cps\nOff cutoff: %i cps\n" % (oncounts_cutoff/(timetrace_binsize*1e-9), offcounts_cutoff/(timetrace_binsize*1e-9))
#	print >> sys.stderr, "Total counts: %i\nOn counts: %i\nOff counts: %i\n" % (len(dtime_ns),len(oncounts_dtime_ns),len(offcounts_dtime_ns))
	
	print >> sys.stderr, split_cutoffs
	
	testcounts = 0
	
	for i in xrange (0, lifetime_times[1].size-1):
		print lifetime_times[1][i],
		for j in xrange (1, args.split+1):
			testcounts += lifetime_counts[j][i]
			print "\t",
			print lifetime_counts[j][i],
		print "\n",
		#print "%g\t%i\t%i" % (lifetime_times[i], lifetime_oncounts[i], lifetime_offcounts[i])	

	print >> sys.stderr, testcounts

else:
	# compute lifetime for all counts
	(lifetime_counts, lifetime_times) = np.histogram(dtime_ns, lifetime_bins)
	for i in xrange (0, lifetime_times.size-1):
		print "%g\t%i" % (lifetime_times[i], lifetime_counts[i])

print >> sys.stderr, "...done printing data.\n"
