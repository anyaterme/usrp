
import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import settings
import datetime
#matplotlib.use('TKAgg')
import sys

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
	print "MUESTRAS ", rates



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


line = None
x = None
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

generate_animation()
