import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fftsize=1024
freq = 2048e6
frames = 2
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
	rates = rates - 1
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

previous= 0
aux = generate_data()
fig1 = plt.figure()
plt.xlim(0, fftsize)
plt.ylim(-200, 20)
print (int(frames*1./freq))
#line_ani = animation.FuncAnimation(fig1, update_data, rates, fargs=(data, aux), interval=int(1000.0/frames), blit=True, repeat=False)
line_ani = animation.FuncAnimation(fig1, update_data, rates, fargs=(data, None), interval=1, blit=True, repeat=False)
plt.show()

