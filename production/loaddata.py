import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
#matplotlib.use('TKAgg')



fftsize=1024
freq = 2048e6
frames = 1
data = None
previous = 0
rates = 0

debug = True

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

def multi_file ():
	import glob, os
	path = "./"
	os.chdir(path)

	averages=[]
	for file in glob.glob("univer*.dat"):
		print(file)
		dataFile = np.fromfile(file, np.float32)
		print dataFile.size
		rates = dataFile.size /fftsize /frames
		rates = rates - 1
		data = np.empty([rates, fftsize*frames])
		for i in range(rates):
			aux = dataFile[i*(fftsize*frames):(i+1)*fftsize*frames]
			data[i] = (np.asarray(aux))
			averages = averages + [np.average(data[i])]
	fig1 = plt.figure()
	plt.xlim(0, len(averages))
	plt.ylim(-140, 0)
	plt.plot(averages)
	plt.title("Duracion: %d horas, %d minutos, %s segundos" % (len(averages)/3600, (len(averages) % 3600) /60, len(averages) % 60))
	plt.show()

#bytime()
multi_file()



#aux = generate_data()
#fig1 = plt.figure()
#plt.xlim(0, fftsize)
#plt.ylim(-200, 20)
##line_ani = animation.FuncAnimation(fig1, update_data, rates, fargs=(data, aux), interval=int(1000.0/frames), blit=True, repeat=False)
#line_ani = animation.FuncAnimation(fig1, update_data, rates, fargs=(data, None), interval=1, blit=True, repeat=False)
#plt.show()

