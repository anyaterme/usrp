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

 		self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*fft_size, filepath, False)
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

def writeHeaderData(filepath, list_freq, tb, time_between_freqs):
	filepath = "%s.hdr" % filepath
	file = open (filepath, "w")
	header = {}
	header["list_freq"] = list_freq
	header["time_between_freqs"] = time_between_freqs
	header["samp_rate"] = tb.samp_rate
	header["center_freq"] = tb.tunning
	header["frame_rate"] = tb.frame_rate
	header["channels"] = tb.fft_size
	file.write(str(header))
	file.close()


if __name__ == '__main__':

	tbtwfreq = 60

	code_date_format = "%Y%m%d%H"
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	list_freq = range (10, 100, 8)
	index = 0
	codeFile = "./DATA-%s.dat" % datetime.datetime.now().strftime(code_date_format)
	tb = listening(_center_freq=list_freq[index % len(list_freq)], filepath=codeFile)
	writeHeaderData (codeFile, list_freq, tb, tbtwfreq)
	nbc = NonBlockingConsole()
	print "Press any key to quit."
	print "Listening to %d MHz..." % list_freq[index % len(list_freq)]
	tb.start()
	tb.set_tunning(list_freq[index % len(list_freq)])
	initial_time = time.time()
	while (True):
		current_codeFile = "./DATA-%s.dat" % datetime.datetime.now().strftime(code_date_format)
		if (current_codeFile != codeFile):
			codeFile = current_codeFile
			tb.stop()
			tb.wait()
			tb = listening(_center_freq=list_freq[index % len(list_freq)], filepath=codeFile)
			writeHeaderData (codeFile, list_freq, tb, tbtwfreq)
			tb.start()
		current_time = time.time()
		if (current_time - initial_time > tbtwfreq):
			index = index + 1
			initial_time = current_time
			print "Listening to %d MHz..." % list_freq[index % len(list_freq)]
			tb.set_tunning(list_freq[index % len(list_freq)])
			
		if nbc.get_data() != False:
			break
	tb.stop()
	tb.wait()

