#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Danifft
# Generated: Tue Jun 30 13:41:17 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
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

class danifft(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Danifft")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Danifft")
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

        self.settings = Qt.QSettings("GNU Radio", "danifft")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.tunning = tunning = 103.3e6
        self.samp_rate = samp_rate = 4e6
        self.range_freq = range_freq = 0
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
        self.uhd_usrp_source_0.set_subdev_spec("A:A", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(tunning, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        self._range_freq_layout = Qt.QVBoxLayout()
        self._range_freq_tool_bar = Qt.QToolBar(self)
        self._range_freq_layout.addWidget(self._range_freq_tool_bar)
        self._range_freq_tool_bar.addWidget(Qt.QLabel("range_freq"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._range_freq_counter = qwt_counter_pyslot()
        self._range_freq_counter.setRange(-50, 50, 1)
        self._range_freq_counter.setNumButtons(2)
        self._range_freq_counter.setValue(self.range_freq)
        self._range_freq_tool_bar.addWidget(self._range_freq_counter)
        self._range_freq_counter.valueChanged.connect(self.set_range_freq)
        self._range_freq_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._range_freq_slider.setRange(-50, 50, 1)
        self._range_freq_slider.setValue(self.range_freq)
        self._range_freq_slider.setMinimumWidth(200)
        self._range_freq_slider.valueChanged.connect(self.set_range_freq)
        self._range_freq_layout.addWidget(self._range_freq_slider)
        self.top_layout.addLayout(self._range_freq_layout)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
        	fft_size, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"QT GUI Plot", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(1)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_f(
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	ref_scale=2,
        	frame_rate=2,
        	avg_alpha=1.0,
        	average=False,
        )
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*fft_size, "/home/laboratorio/develop/usrp/test/fftdani/fftusrp.dat", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.logpwrfft_x_0, 0))


# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "danifft")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tunning(self):
        return self.tunning

    def set_tunning(self, tunning):
        self.tunning = tunning
        self.uhd_usrp_source_0.set_center_freq(self.tunning, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_range_freq(self):
        return self.range_freq

    def set_range_freq(self, range_freq):
        self.range_freq = range_freq
        Qt.QMetaObject.invokeMethod(self._range_freq_counter, "setValue", Qt.Q_ARG("double", self.range_freq))
        Qt.QMetaObject.invokeMethod(self._range_freq_slider, "setValue", Qt.Q_ARG("double", self.range_freq))

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
    tb = danifft()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

