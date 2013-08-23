from _tools import AbstractTool

class Export(AbstractTool):
    def __init__(self):
        self.description = 'outputs a delimited file with the the following headers: # t3_record nsync chan dtime truensync truetime/ns'
    
    def subparse(self, subparser):
        subparser.add_argument("T3", help="you must provide a T3 file as input")
        subparser.add_argument("-a", "--arrivals", help="instead of a delimeted file, print a list of arrival times")
        subparser.add_argument("-d", "--delimiter", type=str, default='\t', help="choose a delimiter for output files")
    
    def execute(self, args):
        if (args.arrivals):
            self.print_arrivals()
        else:
            self.print_delimited_file()
    
    def print_delimited_file(self, delimiter='\t'):
        truensync = self.t3.ofltime + self.t3.nsync
        truetime = (truensync * self.t3.syncperiod) + (self.t3.dtimes * self.t3.header['resolution'])
        for i in xrange (0, self.t3.header['records_count']):
            print "%7u\t%08x\t%6.0f\t%2u\t%4u\t%10.0f\t%12.3f" % (i+1, self.t3.records[i], self.t3.nsync[i], self.t3.chan[i], self.t3.dtimes[i], truensync[i], truetime[i])
    
    def print_arrivals(self, delimiter='\t'):
            arrivals = self.t3.arrivals()
            for i in xrange (0, arrivals.size):
                print "%g" % arrivals[i]

def load():
    # loads the current plugin
    return Export()
