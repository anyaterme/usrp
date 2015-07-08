#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Metafile
# Generated: Thu Jul  2 17:30:53 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser

class metafile(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Metafile")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_file_meta_source_0 = blocks.file_meta_source("/Users/danidiaz/Develop/usrp/test/metafile.dat", True, False, "")
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, "metafile.dat", samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", False)
        self.blocks_file_meta_sink_0.set_unbuffered(False)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_file_meta_source_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_file_meta_sink_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = metafile()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
