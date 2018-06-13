import config
from model import Model
from utility_methods import *
import h5py
import numpy as np
import time


def risk_curve_data(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, time=100000):
    data = np.zeros(shape=(runs, repeats, 3), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0] = l_z
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            tissue.excount.fill(0)  # Clear excitation count
            tissue.model_array.fill(0)  # Clear activations
            tissue.activate_pacemaker()  # Initialise new wavefront
            data[i][j][0] = tissue.seed
            for t in range(1, time + 1):
                excitations = tissue.iterate()
                if np.intersect1d(tissue.excount, [2]):
                    maxpos = tissue.maxpos
                    data[i][j][1] = True
                    data[i][j][2] = maxpos[0] * 100000 + maxpos[1] * 1000 + maxpos[2]
                    break
                elif not np.any(excitations == 50):
                    data[i][j][2] = t
                    break
            # print('Run: {0}, Repeat: {1}, Data: {2}'.format(i, j, data[i][j]))
    return data


def gen_risk(runs, repeats, l_z, nu_x_range, nu_yz_range, angle_vars=False,
             time=100000, dir_name="new_risk_homogeneous"):
    if not os.path.exists('data_analysis/{}'.format(dir_name)):
        os.makedirs('data_analysis/{}'.format(dir_name))
    if angle_vars:
        for av in angle_vars[2]:
            with h5py.File('data_analysis/{}/risk, ang_epi={}, ang_endo={}, nu_av={}'.format(
                    dir_name, angle_vars[0], angle_vars[1], av), 'w') as data_file:
                data_file.create_dataset('risk', data=risk_curve_data(
                    runs, repeats, l_z, 1.0, 1.0, [angle_vars[0], angle_vars[1], av], time), dtype='uint32')
    else:
        for x in nu_x_range:
            for yz in nu_yz_range:
                with h5py.File('data_analysis/{}/risk, nu_x={}, nu_yz={}'.format(dir_name, x, yz), 'w') as data_file:
                    data_file.create_dataset('risk'.format(x, yz), data=risk_curve_data(
                        runs, repeats, l_z, x, yz, False, time), dtype='uint32')


if __name__ == '__main__':
    start = time.time()
    gen_risk(runs=1000, repeats=1, l_z=1, nu_x_range=[1.0], nu_yz_range=[0.1], angle_vars=False, time=100000)
    print(time.time() - start)
