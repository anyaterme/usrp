#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: listening
# Author: Daniel Diaz
# Generated: Thu Jul 16 12:34:06 2015
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import time
import datetime
from utils import NonBlockingConsole


class listening(gr.top_block):

	def __init__(self, _samp_rate = 8e6, _frame_rate = 2, _channels = 1024, _center_freq = 10, filepath = None):
		gr.top_block.__init__(self, "listening")
		if (filepath == None):
			filepath = "./DATA-%s.dat" % datetime.datetime.now().strftime("%Y%m%d")

		##################################################
		# Variables
		##################################################
		self.tunning = tunning = _center_freq
		self.samp_rate = samp_rate = _samp_rate
		self.fft_size = fft_size = _channels
		self.frame_rate = frame_rate = _frame_rate

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_source_0 = uhd.usrp_source( device_addr="", stream_args=uhd.stream_args( cpu_format="fc32", channels=range(1),),)
		self.uhd_usrp_source_0.set_clock_source("external", 0)
		self.uhd_usrp_source_0.set_subdev_spec("A:AB", 0)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(tunning*1e6, 0)
		self.uhd_usrp_source_0.set_gain(0, 0)
		self.logpwrfft_x_0 = logpwrfft.logpwrfft_c( sample_rate=samp_rate, fft_size=fft_size, ref_scale=2, frame_rate=frame_rate, avg_alpha=1.0, average=False,)
		self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_float*fft_size, filepath, samp_rate, 1, blocks.GR_FILE_FLOAT, False, 1000000000, "", True)
		self.blocks_file_meta_sink_0.set_unbuffered(False)

		##################################################
		# Connections
		##################################################
		self.connect((self.uhd_usrp_source_0, 0), (self.logpwrfft_x_0, 0))
		self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_meta_sink_0, 0))


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
	tb = listening()
	tb.start()
	initial_time = time.time()
	index = 0
	nbc = NonBlockingConsole()
	list_freq = range (10, 100, 8)
	print "Press any key to quit."
	print "Listening to %d MHz..." % list_freq[index % len(list_freq)]
	while (True):
		current_time = time.time()
		if (current_time - initial_time > 60):
			index = index + 1
			initial_time = current_time
			print "Listening to %d MHz..." % list_freq[index % len(list_freq)]
			tb.set_tunning(list_freq[index % len(list_freq)])
			
		if nbc.get_data() != False:
			break
	tb.stop()
	tb.wait()

