#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Metafile
# Generated: Tue Jul 14 21:42:04 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser

class metafile(gr.top_block):

	def __init__(self, _samp_rate, _frame_rate, _channels, _center_freq = 0, filename="./metafile.dat"):
		gr.top_block.__init__(self, "Metafile")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = _samp_rate
		self.frame_rate = frame_rate = _frame_rate
		self.channels = channels = _channels
		self.center_freq = center_freq = _center_freq

		##################################################
		# Blocks
		##################################################
		self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
			sample_rate=samp_rate,
			fft_size=channels,
			ref_scale=2,
			frame_rate=frame_rate,
			avg_alpha=1.0,
			average=False,
		)
		file_extra = open("%s.hdr_extra" % filename, "w") 
		dict_extra = {'channels':channels, 'frame_rate':frame_rate, 'center_freq':center_freq}
		file_extra.write(str(dict_extra))
		file_extra.close()
		  
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
		self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_float*channels, filename, samp_rate, 1, blocks.GR_FILE_FLOAT, False, 1000000, "", True)
		self.blocks_file_meta_sink_0.set_unbuffered(False)
		self.blocks_add_xx_0 = blocks.add_vcc(1)
		self.analog_sig_source_x_0_2 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1e3, 1, 0)
		self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2e3, 1, 0)
		self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 8e3, 1, 0)
		self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 4e3, 1, 0)
		self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))	
		self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))	
		self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0, 2))	
		self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0, 3))	
		self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0, 4))	
		self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))	
		self.connect((self.blocks_throttle_0, 0), (self.logpwrfft_x_0, 0))	
		self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_meta_sink_0, 0))	


	def get_samp_rate_0(self):
		return self.samp_rate_0

	def set_samp_rate_0(self, samp_rate_0):
		self.samp_rate_0 = samp_rate_0

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
		self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
		self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
		self.analog_sig_source_x_0_2.set_sampling_freq(self.samp_rate)
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)
		self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

	def get_frame_rate(self):
		return self.frame_rate

	def set_frame_rate(self, frame_rate):
		self.frame_rate = frame_rate

	def get_channels(self):
		return self.channels

	def set_channels(self, channels):
		self.channels = channels


if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = metafile(32e3,2,1024,1)
	tb.start()
	try:
		raw_input('Press Enter to quit: ')
	except EOFError:
		pass
	tb.stop()
	tb.wait()
