import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
from scipy.integrate import odeint

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax = Axes3D(fig)
ax.azim = 45
ax.elev = 45
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')
ax.set_xticklabels('')
ax.set_yticklabels('')
ax.set_zticklabels('')
linea, = ax.plot([], [], [], label = 'Lorenz', lw = 0.5)
ax.legend()
ax.set_xlim(-20,20)
ax.set_ylim(-30,30)
ax.set_zlim(0,50)


def integra(ccii, t):
	x = ccii[0]            ## Posicion inicial
	y = ccii[1]            ## Posicion inicial
	z = ccii[2]            ## Posicion inicial
	sigma = 10             ## Parametros que se pueden ver en:
	rho = 28               ## http://en.wikipedia.org/wiki/Lorenz_system
	beta = 8.0/3           ##
	dx = sigma * (y - x)   ## Sistema de ecuaciones
	dy = x * (rho -z) - y  ## diferenciales de
	dz = x * y - beta* z   ## Lorenz
	return [dx, dy, dz]

def anima(i, x0, y0, z0):
	t = np.arange(0, (i + 1) / 10., 0.01) ## Paso temporal
	ccii = [x0, y0, z0]                   ## Posicion inicial
	## Integracion de las
	## ecs. de Lorenz mediante
	## scipy.integrate.odeint
	## http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
	## odeint usa la funcion integra
	## que hemos creado anteriormente
	## con las condiciones iniciales (ccii)
	## y los pasos temporales (t)
	soluc = odeint(integra, ccii, t)
	x = soluc[:,0]                        ## Posicion x
	y = soluc[:,1]                        ## Posicion y
	z = soluc[:,2]                        ## Posicion z
	ax.elev = 45 + i / 2.                 ## Vamos rotando el
	ax.azim = 45 + i / 2.                 ## punto de vista
	linea.set_data(x, y)                  ## Asignamos datos para ir
	linea.set_3d_properties(z)            ## dibujando la trayectoria
	return linea,

anim = animation.FuncAnimation(fig, anima, frames = 500, fargs = (0, 1, 1.05), interval = 5, blit = True)
anim.save('Atractor_de_Lorenz(pybonacci).mp4', fps = 10)
