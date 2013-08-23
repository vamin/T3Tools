import math
import numpy as np

from _tools import AbstractTool

class TimeTrace(AbstractTool):
    def __init__(self):
        self.description = 'outputs a time trace, cps vs seconds'
    
    def subparse(self, subparser):
        subparser.add_argument("T3", help="you must provide a T3 file as input")
        subparser.add_argument("-d", "--delimiter", type=str, default='\t', help="choose a delimiter aside from tab for output files")
        subparser.add_argument("-t", "--timetrace-binsize", type=float, default=10, help="choose a binsize for the timetrace, in ms")
    
    def execute(self, args):
        self.print_timetrace(args.timetrace_binsize, args.delimiter)
    
    def print_timetrace(self, timetrace_binsize, delimiter):
        arrivals = self.t3.arrivals()

        timetrace_binsize = timetrace_binsize * 1e6 # convert ms to ns
        timetrace_nbinmax = int( math.ceil(arrivals[-1]/timetrace_binsize) ) + 1 # number of bins necessary given bin size and last arrival
        timetrace_bins = [0]
        
        for i in xrange (1, timetrace_nbinmax):
            timetrace_bins.append(i*timetrace_binsize)
        
        (timetrace_counts, timetrace_times) = np.histogram(arrivals, timetrace_bins)
        
        # average_count_rate = (sum(timetrace_counts)/(timetrace_binsize*1e-9))/len(timetrace_counts)

        for i in xrange (0, timetrace_times.size-1):
            print "%g%s%g" % (timetrace_times[i]/1e9, delimiter, timetrace_counts[i]/(timetrace_binsize*1e-9))

def load():
    # loads the current plugin
    return TimeTrace()

