#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Analizador con Audio
# Author: Daniel Diaz
# Description: Analizador con Audio
# Generated: Tue Jun  9 14:03:25 2015
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

class uhd_wbfm_receive_800k(gr.top_block, Qt.QWidget):

    def __init__(self, final_freq=110, gain=0, audio_output=""):
        gr.top_block.__init__(self, "Analizador con Audio")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Analizador con Audio")
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

        self.settings = Qt.QSettings("GNU Radio", "uhd_wbfm_receive_800k")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.final_freq = final_freq
        self.gain = gain
        self.audio_output = audio_output

        ##################################################
        # Variables
        ##################################################
        self.initial_freq_2 = initial_freq_2 = 104.3
        self.tun_freq_channel = tun_freq_channel = 0
        self.initial_freq = initial_freq = initial_freq_2
        self.bandwidth = bandwidth = 0
        self.tun_freq = tun_freq = initial_freq + (tun_freq_channel)*pow(2,1+bandwidth)
        self.volume = volume = 1
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = tun_freq
        self.tun_gain = tun_gain = 10
        self.samp_rate = samp_rate = pow(2,2+bandwidth)*1e6
        self.num_channels = num_channels = 16
        self.filter_decim = filter_decim = int(pow(2,2+bandwidth)*1e6/400e3)
        self.audio_decim = audio_decim = 10

        ##################################################
        # Blocks
        ##################################################
        self._volume_layout = Qt.QVBoxLayout()
        self._volume_knob = Qwt.QwtKnob()
        self._volume_knob.setRange(0, 10, 0.1)
        self._volume_knob.setValue(self.volume)
        self._volume_knob.valueChanged.connect(self.set_volume)
        self._volume_layout.addWidget(self._volume_knob)
        self._volume_label = Qt.QLabel("Volume")
        self._volume_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)
        self._volume_layout.addWidget(self._volume_label)
        self.top_grid_layout.addLayout(self._volume_layout, 7,3,1,1)
        self._tun_gain_layout = Qt.QVBoxLayout()
        self._tun_gain_knob = Qwt.QwtKnob()
        self._tun_gain_knob.setRange(0, 20, 1)
        self._tun_gain_knob.setValue(self.tun_gain)
        self._tun_gain_knob.valueChanged.connect(self.set_tun_gain)
        self._tun_gain_layout.addWidget(self._tun_gain_knob)
        self._tun_gain_label = Qt.QLabel("UHD Gain")
        self._tun_gain_label.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignHCenter)
        self._tun_gain_layout.addWidget(self._tun_gain_label)
        self.top_grid_layout.addLayout(self._tun_gain_layout, 7,2,1,1)
        self._bandwidth_options = range(4)
        self._bandwidth_labels = ['2','4','8','16']
        self._bandwidth_group_box = Qt.QGroupBox("Channel BandWidth")
        self._bandwidth_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._bandwidth_button_group = variable_chooser_button_group()
        self._bandwidth_group_box.setLayout(self._bandwidth_box)
        for i, label in enumerate(self._bandwidth_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._bandwidth_box.addWidget(radio_button)
        	self._bandwidth_button_group.addButton(radio_button, i)
        self._bandwidth_callback = lambda i: Qt.QMetaObject.invokeMethod(self._bandwidth_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._bandwidth_options.index(i)))
        self._bandwidth_callback(self.bandwidth)
        self._bandwidth_button_group.buttonClicked[int].connect(
        	lambda i: self.set_bandwidth(self._bandwidth_options[i]))
        self.top_grid_layout.addWidget(self._bandwidth_group_box, 0,1,1,1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Centra Freq (MHz)"+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self.variable_qtgui_label_0))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 1,0,1,1)
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
        self.uhd_usrp_source_0.set_center_freq((tun_freq)*1e6+bandwidth-bandwidth, 0)
        self.uhd_usrp_source_0.set_gain(tun_gain, 0)
        self._tun_freq_channel_options = range(num_channels)
        self._tun_freq_channel_labels = map(str, self._tun_freq_channel_options)
        self._tun_freq_channel_group_box = Qt.QGroupBox("Channel")
        self._tun_freq_channel_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._tun_freq_channel_button_group = variable_chooser_button_group()
        self._tun_freq_channel_group_box.setLayout(self._tun_freq_channel_box)
        for i, label in enumerate(self._tun_freq_channel_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._tun_freq_channel_box.addWidget(radio_button)
        	self._tun_freq_channel_button_group.addButton(radio_button, i)
        self._tun_freq_channel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._tun_freq_channel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._tun_freq_channel_options.index(i)))
        self._tun_freq_channel_callback(self.tun_freq_channel)
        self._tun_freq_channel_button_group.buttonClicked[int].connect(
        	lambda i: self.set_tun_freq_channel(self._tun_freq_channel_options[i]))
        self.top_grid_layout.addWidget(self._tun_freq_channel_group_box, 0,2,1,6)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=filter_decim,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	(tun_freq)*1e6, #fc
        	pow(2,1+bandwidth)*1e6, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 4,0,2,8)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	(tun_freq)*1e6, #fc
        	pow(2,1+bandwidth)*1e6, #bw
        	"FFT Plot", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, -40)
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2,0,2,8)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, 400e3, 115e3, 30e3, firdes.WIN_HANN, 6.76))
        self._initial_freq_2_layout = Qt.QVBoxLayout()
        self._initial_freq_2_label = Qt.QLabel("Freq (MHz)")
        self._initial_freq_2_slider = Qwt.QwtSlider(None, Qt.Qt.Vertical, Qwt.QwtSlider.LeftScale, Qwt.QwtSlider.BgSlot)
        self._initial_freq_2_slider.setRange(1, 250, 0.1)
        self._initial_freq_2_slider.setValue(self.initial_freq_2)
        self._initial_freq_2_slider.setMinimumHeight(200)
        self._initial_freq_2_slider.valueChanged.connect(self.set_initial_freq_2)
        self._initial_freq_2_label.setAlignment(Qt.Qt.AlignTop)
        self._initial_freq_2_layout.addWidget(self._initial_freq_2_slider)
        self._initial_freq_2_layout.addWidget(self._initial_freq_2_label)
        self.top_grid_layout.addLayout(self._initial_freq_2_layout, 0,9,10,1)
        self._initial_freq_tool_bar = Qt.QToolBar(self)
        self._initial_freq_tool_bar.addWidget(Qt.QLabel("Initial Freq (MHz)"+": "))
        self._initial_freq_line_edit = Qt.QLineEdit(str(self.initial_freq))
        self._initial_freq_tool_bar.addWidget(self._initial_freq_line_edit)
        self._initial_freq_line_edit.returnPressed.connect(
        	lambda: self.set_initial_freq(eng_notation.str_to_num(self._initial_freq_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._initial_freq_tool_bar, 0,0,1,1)
        self.blocks_multiply_const_vxx = blocks.multiply_const_vff((volume, ))
        self.audio_sink = audio.sink(int(400e3/audio_decim), audio_output, True)
        self.analog_wfm_rcv = analog.wfm_rcv(
        	quad_rate=400e3,
        	audio_decimation=audio_decim,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv, 0))
        self.connect((self.analog_wfm_rcv, 0), (self.blocks_multiply_const_vxx, 0))
        self.connect((self.blocks_multiply_const_vxx, 0), (self.audio_sink, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))


# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "uhd_wbfm_receive_800k")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_final_freq(self):
        return self.final_freq

    def set_final_freq(self, final_freq):
        self.final_freq = final_freq

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_audio_output(self):
        return self.audio_output

    def set_audio_output(self, audio_output):
        self.audio_output = audio_output

    def get_initial_freq_2(self):
        return self.initial_freq_2

    def set_initial_freq_2(self, initial_freq_2):
        self.initial_freq_2 = initial_freq_2
        self.set_initial_freq(self.initial_freq_2)
        Qt.QMetaObject.invokeMethod(self._initial_freq_2_slider, "setValue", Qt.Q_ARG("double", self.initial_freq_2))

    def get_tun_freq_channel(self):
        return self.tun_freq_channel

    def set_tun_freq_channel(self, tun_freq_channel):
        self.tun_freq_channel = tun_freq_channel
        self.set_tun_freq(self.initial_freq + (self.tun_freq_channel)*pow(2,1+self.bandwidth))
        self._tun_freq_channel_callback(self.tun_freq_channel)

    def get_initial_freq(self):
        return self.initial_freq

    def set_initial_freq(self, initial_freq):
        self.initial_freq = initial_freq
        self.set_tun_freq(self.initial_freq + (self.tun_freq_channel)*pow(2,1+self.bandwidth))
        Qt.QMetaObject.invokeMethod(self._initial_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.initial_freq)))

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_filter_decim(int(pow(2,2+self.bandwidth)*1e6/400e3))
        self.set_samp_rate(pow(2,2+self.bandwidth)*1e6)
        self.set_tun_freq(self.initial_freq + (self.tun_freq_channel)*pow(2,1+self.bandwidth))
        self.qtgui_waterfall_sink_x_0.set_frequency_range((self.tun_freq)*1e6, pow(2,1+self.bandwidth)*1e6)
        self._bandwidth_callback(self.bandwidth)
        self.uhd_usrp_source_0.set_center_freq((self.tun_freq)*1e6+self.bandwidth-self.bandwidth, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range((self.tun_freq)*1e6, pow(2,1+self.bandwidth)*1e6)

    def get_tun_freq(self):
        return self.tun_freq

    def set_tun_freq(self, tun_freq):
        self.tun_freq = tun_freq
        self.set_variable_qtgui_label_0(self.tun_freq)
        self.qtgui_waterfall_sink_x_0.set_frequency_range((self.tun_freq)*1e6, pow(2,1+self.bandwidth)*1e6)
        self.uhd_usrp_source_0.set_center_freq((self.tun_freq)*1e6+self.bandwidth-self.bandwidth, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range((self.tun_freq)*1e6, pow(2,1+self.bandwidth)*1e6)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        Qt.QMetaObject.invokeMethod(self._volume_knob, "setValue", Qt.Q_ARG("double", self.volume))
        self.blocks_multiply_const_vxx.set_k((self.volume, ))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_0)))

    def get_tun_gain(self):
        return self.tun_gain

    def set_tun_gain(self, tun_gain):
        self.tun_gain = tun_gain
        Qt.QMetaObject.invokeMethod(self._tun_gain_knob, "setValue", Qt.Q_ARG("double", self.tun_gain))
        self.uhd_usrp_source_0.set_gain(self.tun_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_num_channels(self):
        return self.num_channels

    def set_num_channels(self, num_channels):
        self.num_channels = num_channels

    def get_filter_decim(self):
        return self.filter_decim

    def set_filter_decim(self, filter_decim):
        self.filter_decim = filter_decim

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
    parser.add_option("", "--final-freq", dest="final_freq", type="eng_float", default=eng_notation.num_to_str(110),
        help="Set final_freq [default=%default]")
    parser.add_option("-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set Default Gain [default=%default]")
    parser.add_option("-O", "--audio-output", dest="audio_output", type="string", default="",
        help="Set Audio Output Device [default=%default]")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = uhd_wbfm_receive_800k(final_freq=options.final_freq, gain=options.gain, audio_output=options.audio_output)
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

