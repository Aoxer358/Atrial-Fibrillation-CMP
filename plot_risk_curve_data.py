import h5py
import matplotlib.pyplot as plt
import numpy as np
import glob

nu_yz_val = np.arange(0.005, 1, 0.01)
nu_x_val = np.arange(0.005, 1, 0.01)
X, Y = np.meshgrid(nu_x_val, nu_yz_val)
Z = np.zeros(X.shape)
time = np.zeros_like(Z)
var = np.zeros_like(Z)
wabwab = np.zeros(X.shape)
avz = np.zeros_like(Z)
varz = np.zeros_like(Z)
end_time = np.zeros_like(Z)

example = 'data_analysis/afinduced_data/risk_curve_data_25_0100_0500_False_10000_eb8610e35046e63f'
files = glob.glob('data_analysis/afinduced_data/risk_curve_data_1000_25*')
num_succ = 0
non_zero = 0

for yi in range(len(nu_yz_val)):
    for xi in range(len(nu_x_val)):
        x = X[xi, yi]
        y = Y[xi, yi]

        try:
            start = 'data_analysis/afinduced_data/risk_curve_data_1000_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
            filename = glob.glob(start)[0]
            # print(filename)
            risk_data = np.load(filename)
            ave = np.average(risk_data[:, 1])
            var[yi, xi] = np.std(risk_data[:, 1])
            fib = risk_data[risk_data[:, 1] == 1]
            no_fib = risk_data[(risk_data[:, 1] == 0) & (risk_data[:, -1] == 1)]
            time[yi, xi] = np.average(fib[:, 5])
            end_time[yi, xi] = np.average(no_fib[:, 5])
            normz = (np.absolute((fib[:, 2]).astype('int') - 12))
            avz[yi, xi] = np.average(normz)
            varz[yi, xi] = np.std(normz)

        except:
            ave = 0
            pass
        Z[yi, xi] = ave - .5 * (ave == 0)
        # if 0.36 * x * x - 0.79 * x + 0.25 <= y <= 0.375 * x * x - 0.825 * x + 0.65:
        #     wabwab[xi,yi] = True

# res = 0.36*X*X - 0.79*X +0.43 <= Y <= 0.375*X*X - 0.825*X +0.65
plt.imshow(Z, extent=(0, 1, 0, 1), origin='lower', zorder=1)
plt.title('Risk curve')
# plt.contour(X,Y,Z, levels=[.1,.9], colors='w')
grid_args = dict(color='w',
                 alpha=.4)
plt.plot(nu_x_val, nu_x_val*np.tan(15*np.pi/180), **grid_args)
plt.plot(nu_x_val, nu_x_val*np.tan(30*np.pi/180), **grid_args)
plt.plot(nu_x_val, nu_x_val*np.tan(45*np.pi/180), **grid_args)
plt.plot(nu_x_val, nu_x_val*np.tan(60*np.pi/180), **grid_args)
plt.plot(nu_x_val, nu_x_val*np.tan(75*np.pi/180), **grid_args)
plt.plot(nu_x_val,1-nu_x_val*2,  **grid_args)
plt.plot(nu_x_val,.75-nu_x_val*2,  **grid_args)
plt.plot(nu_x_val,.5-nu_x_val*2,  **grid_args)
plt.plot(nu_x_val,.25-nu_x_val*2,  **grid_args)
plt.xlim((0,1))
plt.ylim((0,1))


plt.figure()
plt.imshow(time, extent=(0, 1, 0, 1), origin='lower', zorder=3)
plt.title('Time to fibrillation')
plt.clim((100., 220.))
# plt.imshow(wabwab, extent=(0,1,0,1), origin='lower', alpha=.1,zorder=2)
plt.figure()
plt.imshow(avz, extent=(0, 1, 0, 1), origin='lower', vmin=5, vmax=10)
plt.title('Averaege z')

plt.figure()
plt.imshow(varz, extent=(0, 1, 0, 1), origin='lower')
plt.title('variance z')

plt.figure()
plt.imshow(200 /end_time , extent=(0, 1, 0, 1), origin='lower')
plt.title('conduction speed')

plt.show()
