import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import settings
import sys, os, datetime, glob
import pmt
from gnuradio.blocks import parse_file_metadata as pfm

fftsize=1024
frames = 2
data = None
previous = 0
rates = 0
headerDict = None

debug = False

def generate_data(filename="*.dat"):
	global data
	global fftsize
	global rates
	os.chdir(settings.path)

	data = []
	for file in glob.glob(filename):
		print "LOADING HEADER..."
		f = open ("./%s.hdr" % file, "r")
		data_with_header = f.read()
		f.close()
		header = pmt.deserialize_str(data_with_header)
		headerDict = pfm.parse_header(header)
		f = open ("./%s.hdr_extra" % file, "r")
		header_extra = f.read()
		aux = eval (header_extra)
		f.close()
		for key in aux:
			headerDict[key] = aux[key]
		print "LOADING DATA..."
		dataFile = np.fromfile(file, np.float32)
		data = np.concatenate([data,np.asarray(dataFile)])
	rates = data.size /fftsize 
	return headerDict, data, rates



def animate(i):
	aux = data[fftsize*i:fftsize*(i+1)]
	if (aux.size== fftsize):
		line.set_ydata(aux)  # update the data
	return line,

#Init only required for blitting to give a clean slate.
def init():
	global x
	line.set_ydata(np.ma.array(x, mask=True))
	return line,


def generate_animation(path="./", filename="*.dat"):
	global line
	global x
	generate_data(filename)
	fig, ax = plt.subplots()
	plt.xlim(0, fftsize)
	plt.ylim(np.amin(data)*1.1, np.amax(data)*1.1)
	x = np.arange(0,fftsize)
	line, = ax.plot(x, data[0:fftsize])
	ani = animation.FuncAnimation(fig, animate, rates, init_func=init, interval=1, blit=False)
	print datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	ani.save('spectral.mp4')
	print datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	print "FIN ANIMACION"

def generate_frames(data, rates, fftsize, path="./", detection_limit = None):
	global line
	print "GENERATING FRAME "
	print path
	print "\tRemoving older images... "
	for file in glob.glob(path+"/*.png"):
		os.remove(file)
	perc = 0
	for i in range(0,rates):
		fig, ax = plt.subplots()
		plt.xlim(0, fftsize)
		plt.ylim(np.amin(data)*1.1, np.amax(data)*1.1)
		x = np.arange(0,fftsize)
		ydata= data[i*fftsize:(i+1)*fftsize]
		if (x.size == ydata.size):
			line, = ax.plot(x, ydata)
			median = np.empty(x.size)
			median_value = np.median(ydata)
			median.fill(median_value)
			line, = ax.plot(x, median, 'r')
			if (detection_limit != None):
				line, = ax.plot(x, median * (1-detection_limit), 'g')
				block_interferences = detect_signal(ydata, 1, headerDict, detection_limit)
				block_array = np.empty(block_interferences.size)
				for index in range(block_interferences.size):
					block_array[index] = ydata[block_interferences[index]]
				ax.scatter(block_interferences, block_array)

#				block_array = np.empty(x.size)
#				block_array.fill(np.min(ydata))
#				for index in block_interferences:
#					block_array[index] = 0
#				line, = ax.plot(x, block_array, 'black')
			plt.savefig(os.path.join(path, "image%05d.png" % i))
			plt.close()
			if int(i*1.0/rates*100.0) != perc:
				perc = int(i*1.0/rates*100.0)
				print "%d%% completed...." % perc

def detect_signal(data, rates, headerDict, detection_limit = 0.1, print_msg = False):
	if (print_msg):
		print "DETECTING SIGNALS..."
	perc = 0
	positives = []
	fftsize = headerDict['channels']
	for i in range(0,rates):
		ydata= data[i*fftsize:(i+1)*fftsize]
		if (fftsize == ydata.size):
			median_value = np.median(ydata)
			aux, = np.where(ydata > median_value * (1-detection_limit))
			positives = np.concatenate([positives, aux])
			if (int(i*1.0/rates*100.0) != perc) and (print_msg):
				perc = int(i*1.0/rates*100.0)
				#print "%d%% completed...." % perc
	positives = np.unique(positives)
	if (print_msg):
		samp_rate = headerDict["rx_rate"]
		center_freq = headerDict["center_freq"]
		channel_width = samp_rate / fftsize
		print "Signal detected in:"
		for index in positives:
			print "Channel %d => %d Hz" % (index, index * channel_width)
		
	return positives
	


line = None
x = None

if (__name__ == '__main__'):
	#generate_animation("./fttusrp.dat")
	headerDict, data, rates = generate_data("DATA-20150716.dat")
	#detect_signal(data, rates, headerDict, 0.1, True)
	generate_frames(data, rates, fftsize, "./images", 0.1)
	
