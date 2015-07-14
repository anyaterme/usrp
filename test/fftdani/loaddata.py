import matplotlib
#matplotlib.use('Agg')
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
	dataFile = np.fromfile('./fftusrp.dat', np.float32)
	if debug:
		print dataFile
	rates = dataFile.size /fftsize 
	rates = rates 
	data = np.empty([rates, fftsize])
	for i in range(rates):
		aux = dataFile[i*fftsize:(i+1)*fftsize]
		data[i] = (np.asarray(aux))
	return aux

def update_data (num, data, aux):
	#aux = plt.plot(data[num], 'r')
	y_value = np.average(data[num])
	aux = plt.plot([num],[y_value],'ro')
	return aux

def bytime():
	dataFile = np.fromfile('./fftusrp.dat', np.float32)
	if debug:
		print "Data:", dataFile
	rates = dataFile.size /fftsize /frames
	rates = rates - 1
	data = np.empty([rates, fftsize*frames])
	averages = np.empty(rates)
	for i in range(rates):
		aux = dataFile[i*(fftsize*frames):(i+1)*fftsize*frames]
		data[i] = (np.asarray(aux))
		averages[i] = np.average(data[i])
	if debug:
		print "Averages:", averages
	
	fig1 = plt.figure()
	plt.plot(averages)
	plt.show()

def multi_file (time=0):
	import glob, os
	path = settings.path
	os.chdir(path)

	averages=[]
	for file in glob.glob("fftusrp.dat"):
		if debug:
			print(file)
		dataFile = np.fromfile(file, np.float32)
		if debug:
			print dataFile.size
		rates = dataFile.size /fftsize /frames
		rates = rates - 1
		data = np.empty([rates, fftsize*frames])
		if (time == 0):
			for i in range(rates):
				aux = dataFile[i*(fftsize*frames):(i+1)*fftsize*frames]
				data[i] = (np.asarray(aux))
				averages = averages + [np.average(data[i])]
		else:
			for i in range(rates - time, rates):
				aux = dataFile[i*(fftsize*frames):(i+1)*fftsize*frames]
				data[i] = (np.asarray(aux))
				averages = averages + [np.average(data[i])]
	if debug:
		print "Preparando figura"
	fig1 = plt.figure()
	plt.xlim(0, len(averages))
	plt.ylim(-140, 80)
	plt.plot(averages)
	plt.title("Duracion: %d horas, %d minutos, %s segundos\nHora actual: %s" % (len(averages)/3600, (len(averages) % 3600) /60, len(averages) % 60, datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")))
	#plt.show()
	plt.savefig('%stest%d.png' % (settings.path, time))

def test(time=0):
	dataFile = np.fromfile('./fftusrp.dat', np.float32)
	debug = True
	rates = dataFile.size /fftsize /frames
	rates = rates - 1
	if (time == 0):
		data = np.asarray(dataFile)
	else:
		data = np.asarray(dataFile[dataFile.size-time*frames*fftsize:])
	if debug:
		print "Data:", dataFile, dataFile.size, fftsize, frames, data.size
	fig1 = plt.figure()
	plt.plot(data)
	plt.show()


#bytime()
#multi_file(time=600)
#multi_file(time=3600)
#multi_file(time=3600*5)
#multi_file()




#aux = generate_data()
#fig1 = plt.figure()
#plt.xlim(0, fftsize)
#plt.ylim(-200, 20)
##line_ani = animation.FuncAnimation(fig1, update_data, rates, fargs=(data, aux), interval=int(1000.0/frames), blit=True, repeat=False)
#line_ani = animation.FuncAnimation(fig1, update_data, rates, fargs=(data, None), interval=1, blit=True, repeat=False)
#plt.show()
#


