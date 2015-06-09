import numpy as np
import matplotlib.pyplot as plt

freq = 32e3
data = np.fromfile('./test.dat', np.complex64)
print data
divBySeconds = 16
muestreo = freq / divBySeconds
intervals = int (len(data) / muestreo )
print muestreo
print "Seconds ", int(len(data) / freq)

values=[]
for interval in range(1,intervals):
	#value = np.mean(data.real[interval*muestreo:interval*(muestreo+ 1)])
	value = (data.real[interval*muestreo])
	values.append(value)
	

plt.plot(values)
plt.show()

FFT = abs(np.fft.fft(data))
freqs = np.fft.fftfreq(data.size, 1/freq)
plt.plot(freqs, 20*np.log10(FFT))
plt.show()
