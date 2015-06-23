#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Fromfile
# Generated: Tue Mar 31 12:33:06 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
import argparse
import wx

class fromfile(grc_wxgui.top_block_gui):

	def __init__(self, filepath, center_freq):
		grc_wxgui.top_block_gui.__init__(self, title="Fromfile")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 4e6
		self.center_freq = center_freq 

		##################################################
		# Blocks
		##################################################
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.GetWin(),
			baseband_freq=center_freq*1e6,
			dynamic_range=100,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
			win=window.blackmanharris,
			size=(400,400),
		)
		self.GridAdd(self.wxgui_waterfallsink2_0.win, 0, 0, 1, 1)
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=samp_rate,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=1,
			trig_mode=wxgui.TRIG_MODE_AUTO,
			y_axis_label="Counts",
			size=(800,400),
		)
		self.GridAdd(self.wxgui_scopesink2_0.win, 1, 0, 1, 2)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=center_freq*1e6,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
			win=window.hamming,
			size=(400,400),
		)
		self.GridAdd(self.wxgui_fftsink2_0.win, 0, 1, 1, 1)
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
		self.blocks_file_source_1 = blocks.file_source(gr.sizeof_gr_complex*1, "./usrp.dat", True)
		self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

		##################################################
		# Connections
		##################################################
		self.connect((self.blocks_complex_to_float_0, 0), (self.wxgui_scopesink2_0, 0))
		self.connect((self.blocks_file_source_1, 0), (self.blocks_throttle_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_float_0, 0))


# QT sink close method reimplementation

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)

	def get_center_freq(self):
		return self.center_freq

	def set_center_freq(self, center_freq):
		self.center_freq = center_freq
		self.wxgui_waterfallsink2_0.set_baseband_freq(self.center_freq*1e6)
		self.wxgui_fftsink2_0.set_baseband_freq(self.center_freq*1e6)

if __name__ == '__main__':
	import ctypes
	import sys
	if sys.platform.startswith('linux'):
		try:
			x11 = ctypes.cdll.LoadLibrary('libX11.so')
			x11.XInitThreads()
		except:
			print "Warning: failed to XInitThreads()"
	parser = argparse.ArgumentParser(description='Read data from USRP.')
	parser.add_argument('--file', '-f', default="./usrp.dat", type=str, help = "datafile path", required=True)
	parser.add_argument('--freq', default=25, type=float, help = "Center Freq in Mhz", required=True)
	args = parser.parse_args()
	tb = fromfile(filepath=args.file, center_freq=args.freq)
	tb.Start(True)
	tb.Wait()

