#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: UHD WBFM Receive
# Author: Example
# Description: WBFM Receive
# Generated: Fri Jan 30 18:00:50 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import sip
import sys
import time

from distutils.version import StrictVersion
class uhd_wbfm_receive(gr.top_block, Qt.QWidget):

    def __init__(self, address="addr=192.168.10.2", samp_rate=400e3, gain=0, audio_output="", freq=93.3e6):
        gr.top_block.__init__(self, "UHD WBFM Receive")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("UHD WBFM Receive")
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

        self.settings = Qt.QSettings("GNU Radio", "uhd_wbfm_receive")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.address = address
        self.samp_rate = samp_rate
        self.gain = gain
        self.audio_output = audio_output
        self.freq = freq

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.tun_gain = tun_gain = 10
        self.tun_freq = tun_freq = freq/1e6
        self.fine = fine = 0
        self.audio_decim = audio_decim = 10

        ##################################################
        # Blocks
        ##################################################
        self._volume_layout = Qt.QVBoxLayout()
        self._volume_tool_bar = Qt.QToolBar(self)
        self._volume_layout.addWidget(self._volume_tool_bar)
        self._volume_tool_bar.addWidget(Qt.QLabel("Volume"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._volume_counter = qwt_counter_pyslot()
        self._volume_counter.setRange(0, 10, 0.1)
        self._volume_counter.setNumButtons(2)
        self._volume_counter.setValue(self.volume)
        self._volume_tool_bar.addWidget(self._volume_counter)
        self._volume_counter.valueChanged.connect(self.set_volume)
        self._volume_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._volume_slider.setRange(0, 10, 0.1)
        self._volume_slider.setValue(self.volume)
        self._volume_slider.setMinimumWidth(200)
        self._volume_slider.valueChanged.connect(self.set_volume)
        self._volume_layout.addWidget(self._volume_slider)
        self.top_grid_layout.addLayout(self._volume_layout, 1, 0, 1, 4)
        self._tun_gain_layout = Qt.QVBoxLayout()
        self._tun_gain_tool_bar = Qt.QToolBar(self)
        self._tun_gain_layout.addWidget(self._tun_gain_tool_bar)
        self._tun_gain_tool_bar.addWidget(Qt.QLabel("UHD Gain"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._tun_gain_counter = qwt_counter_pyslot()
        self._tun_gain_counter.setRange(0, 20, 1)
        self._tun_gain_counter.setNumButtons(2)
        self._tun_gain_counter.setValue(self.tun_gain)
        self._tun_gain_tool_bar.addWidget(self._tun_gain_counter)
        self._tun_gain_counter.valueChanged.connect(self.set_tun_gain)
        self._tun_gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._tun_gain_slider.setRange(0, 20, 1)
        self._tun_gain_slider.setValue(self.tun_gain)
        self._tun_gain_slider.setMinimumWidth(200)
        self._tun_gain_slider.valueChanged.connect(self.set_tun_gain)
        self._tun_gain_layout.addWidget(self._tun_gain_slider)
        self.top_layout.addLayout(self._tun_gain_layout)
        self._tun_freq_layout = Qt.QVBoxLayout()
        self._tun_freq_tool_bar = Qt.QToolBar(self)
        self._tun_freq_layout.addWidget(self._tun_freq_tool_bar)
        self._tun_freq_tool_bar.addWidget(Qt.QLabel("UHD Freq (MHz)"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._tun_freq_counter = qwt_counter_pyslot()
        self._tun_freq_counter.setRange(10, 250, 1)
        self._tun_freq_counter.setNumButtons(2)
        self._tun_freq_counter.setValue(self.tun_freq)
        self._tun_freq_tool_bar.addWidget(self._tun_freq_counter)
        self._tun_freq_counter.valueChanged.connect(self.set_tun_freq)
        self._tun_freq_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._tun_freq_slider.setRange(10, 250, 1)
        self._tun_freq_slider.setValue(self.tun_freq)
        self._tun_freq_slider.setMinimumWidth(200)
        self._tun_freq_slider.valueChanged.connect(self.set_tun_freq)
        self._tun_freq_layout.addWidget(self._tun_freq_slider)
        self.top_grid_layout.addLayout(self._tun_freq_layout, 0,0,1,2)
        self._fine_layout = Qt.QVBoxLayout()
        self._fine_tool_bar = Qt.QToolBar(self)
        self._fine_layout.addWidget(self._fine_tool_bar)
        self._fine_tool_bar.addWidget(Qt.QLabel("Fine Freq (MHz)"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._fine_counter = qwt_counter_pyslot()
        self._fine_counter.setRange(-.1, .1, .01)
        self._fine_counter.setNumButtons(2)
        self._fine_counter.setValue(self.fine)
        self._fine_tool_bar.addWidget(self._fine_counter)
        self._fine_counter.valueChanged.connect(self.set_fine)
        self._fine_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._fine_slider.setRange(-.1, .1, .01)
        self._fine_slider.setValue(self.fine)
        self._fine_slider.setMinimumWidth(200)
        self._fine_slider.valueChanged.connect(self.set_fine)
        self._fine_layout.addWidget(self._fine_slider)
        self.top_grid_layout.addLayout(self._fine_layout, 0,2,1,2)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_subdev_spec("A:AB", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq((tun_freq+fine)*1e6, 0)
        self.uhd_usrp_source_0.set_gain(tun_gain, 0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	(tun_freq+fine)*1e6, #fc
        	samp_rate, #bw
        	"FFT Plot", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2,0,2,4)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 115e3, 30e3, firdes.WIN_HANN, 6.76))
        self.blocks_multiply_const_vxx = blocks.multiply_const_vff((volume, ))
        self.audio_sink = audio.sink(int(samp_rate/audio_decim), audio_output, True)
        self.analog_wfm_rcv = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=audio_decim,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv, 0), (self.blocks_multiply_const_vxx, 0))    
        self.connect((self.blocks_multiply_const_vxx, 0), (self.audio_sink, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhd_wbfm_receive")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range((self.tun_freq+self.fine)*1e6, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 115e3, 30e3, firdes.WIN_HANN, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_audio_output(self):
        return self.audio_output

    def set_audio_output(self, audio_output):
        self.audio_output = audio_output

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_tun_freq(self.freq/1e6)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx.set_k((self.volume, ))
        Qt.QMetaObject.invokeMethod(self._volume_counter, "setValue", Qt.Q_ARG("double", self.volume))
        Qt.QMetaObject.invokeMethod(self._volume_slider, "setValue", Qt.Q_ARG("double", self.volume))

    def get_tun_gain(self):
        return self.tun_gain

    def set_tun_gain(self, tun_gain):
        self.tun_gain = tun_gain
        Qt.QMetaObject.invokeMethod(self._tun_gain_counter, "setValue", Qt.Q_ARG("double", self.tun_gain))
        Qt.QMetaObject.invokeMethod(self._tun_gain_slider, "setValue", Qt.Q_ARG("double", self.tun_gain))
        self.uhd_usrp_source_0.set_gain(self.tun_gain, 0)

    def get_tun_freq(self):
        return self.tun_freq

    def set_tun_freq(self, tun_freq):
        self.tun_freq = tun_freq
        self.qtgui_freq_sink_x_0.set_frequency_range((self.tun_freq+self.fine)*1e6, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq((self.tun_freq+self.fine)*1e6, 0)
        Qt.QMetaObject.invokeMethod(self._tun_freq_counter, "setValue", Qt.Q_ARG("double", self.tun_freq))
        Qt.QMetaObject.invokeMethod(self._tun_freq_slider, "setValue", Qt.Q_ARG("double", self.tun_freq))

    def get_fine(self):
        return self.fine

    def set_fine(self, fine):
        self.fine = fine
        Qt.QMetaObject.invokeMethod(self._fine_counter, "setValue", Qt.Q_ARG("double", self.fine))
        Qt.QMetaObject.invokeMethod(self._fine_slider, "setValue", Qt.Q_ARG("double", self.fine))
        self.qtgui_freq_sink_x_0.set_frequency_range((self.tun_freq+self.fine)*1e6, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq((self.tun_freq+self.fine)*1e6, 0)

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim

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
    parser.add_option("-a", "--address", dest="address", type="string", default="addr=192.168.10.2",
        help="Set IP Address [default=%default]")
    parser.add_option("-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(400e3),
        help="Set Sample Rate [default=%default]")
    parser.add_option("-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set Default Gain [default=%default]")
    parser.add_option("-O", "--audio-output", dest="audio_output", type="string", default="",
        help="Set Audio Output Device [default=%default]")
    parser.add_option("-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(93.3e6),
        help="Set Default Frequency [default=%default]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = uhd_wbfm_receive(address=options.address, samp_rate=options.samp_rate, gain=options.gain, audio_output=options.audio_output, freq=options.freq)
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
