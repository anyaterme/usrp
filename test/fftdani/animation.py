import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import settings
import sys, os, datetime

fftsize=1024
frames = 2
data = None
previous = 0
rates = 0

debug = False

def generate_data(filename="*.dat"):
	global data
	global fftsize
	global rates
	import glob, os
	os.chdir(settings.path)

	data = []
	for file in glob.glob(filename):
		dataFile = np.fromfile(file, np.float32)
		data = np.concatenate([data,np.asarray(dataFile)])
	rates = data.size /fftsize 



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

def generate_frames(path="./", filename="*.dat"):
	global rates, data, line
	generate_data(filename)
	print "GENERATING FRAME "
	control_point = int(rates * 0.01)
	for i in range(0,rates):
		fig, ax = plt.subplots()
		plt.xlim(0, fftsize)
		plt.ylim(np.amin(data)*1.1, np.amax(data)*1.1)
		x = np.arange(0,fftsize)
		ydata = data[i*fftsize:(i+1)*fftsize]
		if (x.size == ydata.size):
			line, = ax.plot(x, ydata)
			median = np.empty(x.size)
			median.fill(np.median(ydata))
			line, = ax.plot(x, median, 'r')
			plt.savefig(os.path.join(path, "image%05d.png" % i))
			plt.close()
			if i % control_point == 0:
				print "%d% completed...." % (int(i / control_point))

line = None
x = None

#generate_animation("./fttusrp.dat")
generate_frames("./images", "./fftusrpmeta.dat")
