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

def generate_data():
	global data
	global fftsize
	global rates
	import glob, os
	os.chdir(settings.path)

	data = []
	for file in glob.glob("univer*.dat"):
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


def generate_animation():
	global line
	global x
	generate_data()
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

def generate_frames(path="./"):
	global rates, data, line
	generate_data()
	print "GENERATING FRAME "
	for i in range(0,rates):
		print "%05d OF %d" % (i+1, rates),
		fig, ax = plt.subplots()
		plt.xlim(0, fftsize)
		plt.ylim(np.amin(data)*1.1, np.amax(data)*1.1)
		x = np.arange(0,fftsize)
		ydata = data[i*fftsize:(i+1)*fftsize]
		if (x.size == ydata.size):
			line, = ax.plot(x, ydata)
			plt.savefig(os.path.join(path, "image%05d.png" % i))
			plt.close()

line = None
x = None

#generate_animation()
generate_frames("./images")
