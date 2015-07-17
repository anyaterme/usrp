#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: listening
# Author: Daniel Diaz
# Generated: Fri Jul 17 12:05:20 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import time

class listening_gnuradio(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "listening")

        ##################################################
        # Variables
        ##################################################
        self.tunning = tunning = 40
        self.samp_rate = samp_rate = 8e6
        self.fft_size = fft_size = 1024

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	device_addr="",
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_source("external", 0)
        self.uhd_usrp_source_0.set_subdev_spec("A:AB", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(tunning*1e6, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	ref_scale=2,
        	frame_rate=2,
        	avg_alpha=1.0,
        	average=False,
        )
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1024, "/home/laboratorio/develop/usrp/test/fftdani/data.dat", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_sink_0, 0))


# QT sink close method reimplementation

    def get_tunning(self):
        return self.tunning

    def set_tunning(self, tunning):
        self.tunning = tunning
        self.uhd_usrp_source_0.set_center_freq(self.tunning*1e6, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = listening_gnuradio()
    tb.start()
    raw_input('Press Enter to quit: ')
    tb.stop()
    tb.wait()

