import math
import numpy as np

from _tools import AbstractTool

class Lifetime(AbstractTool):
    def __init__(self):
        self.description = 'outputs delimited file of an overall lifetime histogram, or in the case that a cutoff is specified, TSV with separate columns for on and off lifetime histograms (columns are [time/ns] [total or on counts] [off counts])'

    def subparse(self, subparser):
        subparser.add_argument("T3", help="you must provide a T3 file as input")
        subparser.add_argument("-d", "--delimiter", type=str, default='\t', help="choose a delimiter aside from tab for output files")
        subparser.add_argument("-t", "--timetrace-binsize", type=float, default=10, help="choose a binsize for the timetrace, in ms")
        subparser.add_argument("-l", "--lifetime-binsize-mult", type=int, default=10, help="choose a multiple of the resolution (see header output, typically 0.016-0.064ns) as a bin size for the lifetime histogram(s)")
        subparser.add_argument("-c", "--cutoff", type=float, default=0, help="choose an intensity cutoff percentage to output separate \"on\" and \"off\" lifetime histograms")
        subparser.add_argument("-s", "--split", type=int, default=0, help="split into N lifetimes, stratified by bin intensity")
        subparser.add_argument("-z", "--time-zero", type=float, default=0, help="choose a new zero, in ns, to rectify wraparound")

    def execute(self, args):
        dtime_ns = self.t3.corrected_dtimes(args.time_zero)
        lifetime_bins = self.setup_bins(dtime_ns, args.lifetime_binsize_mult)
        
        if (args.cutoff > 0):
            (timetrace_counts, timetrace_times) = self.timetrace(args.timetrace_binsize, args.delimiter)

            timetrace_max = timetrace_counts.max()
            timetrace_min = timetrace_counts.min()

            oncounts_cutoff = timetrace_min + (timetrace_max * (args.cutoff/100))
            offcounts_cutoff = timetrace_min + (timetrace_max * (1-(args.cutoff/100)))
	        
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

            for i in xrange (0, lifetime_times.size-1):
                print "%g\t%i\t%i" % (lifetime_times[i], lifetime_oncounts[i], lifetime_offcounts[i])

        elif (args.split > 0):
            (timetrace_counts, timetrace_times) = self.timetrace(args.timetrace_binsize, args.delimiter)
            
            timetrace_max = timetrace_counts.max()
            timetrace_min = timetrace_counts.min()

            split_cutoffs = [0 for i in range(args.split+1)]
            split_upper = [[] for i in range(args.split+1)]
            split_lower = [[] for i in range(args.split+1)]

            for i in xrange (1, args.split+1):
                split_cutoffs[i] = timetrace_min + (timetrace_max * (i/float(args.split)))
                split_upper[i] = timetrace_counts <= split_cutoffs[i]
                split_lower[i] = timetrace_counts > split_cutoffs[i-1]
	

            j=1 # keep track of what timetrace bin we're in
            split_dtime_ns = [[] for i in range(args.split+1)]
            arrivals = self.t3.arrivals()
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

            for i in xrange (0, lifetime_times[1].size-1):
                print lifetime_times[1][i],
                for j in xrange (1, args.split+1):
                    #testcounts += lifetime_counts[j][i]
                    print "\t",
                    print lifetime_counts[j][i],
                print "\n",
        
        else:
            self.calculate_overall_lifetime(dtime_ns, lifetime_bins, args.delimiter)
    
    def setup_bins(self, dtime_ns, lifetime_binsize_mult):
        # set up lifetime bins
        lifetime_binsize = lifetime_binsize_mult * self.t3.header['resolution'] # ns
        lifetime_binmax = max(dtime_ns) # ns
        lifetime_nbinmax = int( math.ceil(lifetime_binmax / lifetime_binsize) ) + 1

        lifetime_bins = [0]
        for i in xrange (1, lifetime_nbinmax):
	        lifetime_bins.append(i*lifetime_binsize)
        return lifetime_bins
    
    def timetrace(self, timetrace_binsize, delimiter):
        arrivals = self.t3.arrivals()

        timetrace_binsize = timetrace_binsize * 1e6 # convert ms to ns
        timetrace_nbinmax = int( math.ceil(arrivals[-1]/timetrace_binsize) ) + 1 # number of bins necessary given bin size and last arrival
        timetrace_bins = [0]
        
        for i in xrange (1, timetrace_nbinmax):
            timetrace_bins.append(i*timetrace_binsize)
        
        (timetrace_counts, timetrace_times) = np.histogram(arrivals, timetrace_bins)
        return (timetrace_counts, timetrace_times)   
    
    def calculate_overall_lifetime(self, dtime_ns, lifetime_bins, delimiter):
        # compute lifetime for all counts
        (lifetime_counts, lifetime_times) = np.histogram(dtime_ns, lifetime_bins)
        for i in xrange (0, lifetime_times.size-1):
            print "%g%s%i" % (lifetime_times[i], delimiter, lifetime_counts[i])
   

def load():
    """Loads the current tool"""
    return Lifetime()

