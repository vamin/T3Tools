import sys
import numpy as np

class T3(object):
    def __init__(self, T3):
        self.T3 = T3
        self.parse(T3)
    
    def parse(self, T3):
        header = {}
        header_units = {}
        with open(T3, 'rb') as fid:
            #
            # ASCII T3 header
            #
            header['identifier'] = ''.join(map(chr, np.fromfile(fid, np.byte, 16)))
            header['format_version'] = ''.join(map(chr, np.fromfile(fid, np.byte, 6)))
            header['creator_name'] = ''.join(map(chr, np.fromfile(fid, np.byte, 18)))
            header['creator_version'] = ''.join(map(chr, np.fromfile(fid, np.byte, 12)))
            header['file_time'] = ''.join(map(chr, np.fromfile(fid, np.byte, 18)))
            np.fromfile(fid, np.byte, 2) # skip
            header['comment'] = ''.join(map(chr, np.fromfile(fid, np.byte, 256)))
            #
            # binary T3 header
            #
            header['number_of_curves'] = np.fromfile(fid, np.int32, 1)[0]
            header['bits_/_record'] = np.fromfile(fid, np.int32, 1)[0]
            header['routing_channels'] = np.fromfile(fid, np.int32, 1)[0]
            header['number_of_boards'] = np.fromfile(fid, np.int32, 1)[0]
            header['active_curve'] = np.fromfile(fid, np.int32, 1)[0]
            header['measurement_mode'] = np.fromfile(fid, np.int32, 1)[0]
            header['sub-mode'] = np.fromfile(fid, np.int32, 1)[0]
            header['range_no.'] = np.fromfile(fid, np.int32, 1)[0]
            header['offset'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['offset'] = 'ns'
            header['acquisition_time'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['acquisition_time'] = 'ms'
            header['stop_at'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['stop_at'] = 'counts'
            header['stop_on_overflow'] = np.fromfile(fid, np.int32, 1)[0]
            header['restart'] = np.fromfile(fid, np.int32, 1)[0]
            header['display_lin/log'] = np.fromfile(fid, np.int32, 1)[0]
            header['display_time_axis_from'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['display_time_axis_from'] = 'ns'
            header['display_time_axis_to'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['display_time_axis_to'] = 'ns'
            header['display_time_axis_from'] = np.fromfile(fid, np.int32, 1)[0]
            header['display_count_axis_to'] = np.fromfile(fid, np.int32, 1)[0]
            np.fromfile(fid, np.int32, 16) # skip DispCurve stuff
            np.fromfile(fid, np.single, 9) # skip Param stuff
            header['repeat_mode'] = np.fromfile(fid, np.int32, 1)[0]
            header['repeat_/_curve'] = np.fromfile(fid, np.int32, 1)[0]
            header['repeat_time'] = np.fromfile(fid, np.int32, 1)[0]
            header['repeat_wait_time'] = np.fromfile(fid, np.int32, 1)[0]
            header['script_name'] = ''.join(map(chr, np.fromfile(fid, np.byte, 20)))
            #
	        # board specific header
	        #
            header['hardware_identifier'] = ''.join(map(chr, np.fromfile(fid, np.byte, 16)))
            header['hardware_version'] = ''.join(map(chr, np.fromfile(fid, np.byte, 8)))
            header['hw_serial_number'] = np.fromfile(fid, np.int32, 1)[0]
            header['syn_divider'] = np.fromfile(fid, np.int32, 1)[0]
            header['cfd_zero_ch0'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['cfd_zero_ch0'] = 'mV'
            header['cfd_discriminator_ch0'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['cfd_discriminator_ch0'] = 'mV'
            header['cfd_zero_ch1'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['cfd_zero_ch1'] = 'mV'
            header['cfd_discriminator_ch1'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['cfd_discriminator_ch1'] = 'mV'
            header['resolution'] = np.fromfile(fid, np.single, 1)[0]
            header_units['resolution'] = 'ns'
            np.fromfile(fid, np.int32, 26) # skip router settings
            #
	        # T3 mode specific header
	        #
            header['external_devices'] = np.fromfile(fid, np.int32, 1)[0]
            header['reserved1'] = np.fromfile(fid, np.int32, 1)[0]
            header['reserved2'] = np.fromfile(fid, np.int32, 1)[0]
            header['count_rate_ch0'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['count_rate_ch0'] = 'Hz'
            header['count_rate_ch1'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['count_rate_ch1'] = 'Hz'
            header['stop_after'] = np.fromfile(fid, np.int32, 1)[0]
            header_units['stop_after'] = 'ms'
            header['stop_reason'] = np.fromfile(fid, np.int32, 1)[0]
            header['records_count'] = np.fromfile(fid, np.uint32, 1)[0]
            header['imaging_header_size'] = np.fromfile(fid, np.int32, 1)[0]
            #
            # T3 records
            #
            records = np.fromfile(fid, np.uint32, header['records_count'])
            nsync = records & 65535
            chan = (records >> 28) & 15
            dtimes = (records >> 16) & 4095
        
        # set header info    
        self.header = header
        self.header_units = header_units
        
        # set counters and constants
        self.ofltime = cnt_1 = cnt_2 = cnt_3 = cnt_4 = cnt_Ofl = cnt_M = cnt_Err = 0 # counters
        self.wraparound = 65536
        self.syncperiod = 1E9/header['count_rate_ch0'] # in ns
        
        # store and unpack T3 records
        self.records = records
        self.nsync = records & 65535
        self.chan = (records >> 28) & 15
        self.dtimes = (records >> 16) & 4095
        
    def arrivals(self):
        ofltime = np.cumsum(self.chan==15) * self.wraparound
        synctimes = (ofltime + self.nsync) * self.syncperiod
        return self.dtimes[self.chan==1] * self.header['resolution'] + synctimes[self.chan==1]
    
    def corrected_dtimes(self, zero=0):
        # returns delay times in ns, corrected for new zero
        dtime_shift = np.asarray((self.dtimes[self.chan==1] * self.header['resolution']) - zero)
        return np.where(dtime_shift < 0, abs(dtime_shift) + self.syncperiod - zero, dtime_shift)
    
    def report(self):
        # prints formtatted header info to stderr
        for k,v in self.header:
            print >> sys.stderr, k.title(), v

