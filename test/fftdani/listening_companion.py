#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: listening
# Author: Daniel Diaz
# Generated: Thu Jul 16 12:19:02 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import sip
import sys
import time

class listening_companion(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "listening")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("listening")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "listening_companion")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.tunning_gui = tunning_gui = 40
        self.tunning = tunning = tunning_gui
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
        self._tunning_gui_layout = Qt.QVBoxLayout()
        self._tunning_gui_tool_bar = Qt.QToolBar(self)
        self._tunning_gui_layout.addWidget(self._tunning_gui_tool_bar)
        self._tunning_gui_tool_bar.addWidget(Qt.QLabel("tunning_gui"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._tunning_gui_counter = qwt_counter_pyslot()
        self._tunning_gui_counter.setRange(0, 250, 1)
        self._tunning_gui_counter.setNumButtons(2)
        self._tunning_gui_counter.setValue(self.tunning_gui)
        self._tunning_gui_tool_bar.addWidget(self._tunning_gui_counter)
        self._tunning_gui_counter.valueChanged.connect(self.set_tunning_gui)
        self._tunning_gui_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._tunning_gui_slider.setRange(0, 250, 1)
        self._tunning_gui_slider.setValue(self.tunning_gui)
        self._tunning_gui_slider.setMinimumWidth(200)
        self._tunning_gui_slider.valueChanged.connect(self.set_tunning_gui)
        self._tunning_gui_layout.addWidget(self._tunning_gui_slider)
        self.top_layout.addLayout(self._tunning_gui_layout)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        
        
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	ref_scale=2,
        	frame_rate=2,
        	avg_alpha=1.0,
        	average=False,
        )
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_float*1024, "/home/laboratorio/develop/usrp/fftusrpmeta.dat", samp_rate, 1, blocks.GR_FILE_FLOAT, False, 1000000000, "", True)
        self.blocks_file_meta_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_meta_sink_0, 0))


# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "listening_companion")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tunning_gui(self):
        return self.tunning_gui

    def set_tunning_gui(self, tunning_gui):
        self.tunning_gui = tunning_gui
        self.set_tunning(self.tunning_gui)
        Qt.QMetaObject.invokeMethod(self._tunning_gui_counter, "setValue", Qt.Q_ARG("double", self.tunning_gui))
        Qt.QMetaObject.invokeMethod(self._tunning_gui_slider, "setValue", Qt.Q_ARG("double", self.tunning_gui))

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
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = listening_companion()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

