"""
Model of atrial fibrillation

Andrew Ford
"""
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


class Substrate:
    def __init__(self, substrate_size, structural_homogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period, layer_homogenity, seed=False):
        if not seed:
            seed = np.random.randint(0,2**32-1, dtype='uint32')
        self.seed = seed
        self.r = np.random.RandomState(seed)
        self.substrate_size = substrate_size
        self.structural_heterogeneity = structural_homogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = np.int8(refractory_period)
        self.layer_homogenity = layer_homogenity
        self.activation = np.zeros(substrate_size, dtype='int8')  # Grid of activation state
        self.linkage = self.r.choice(a=[True, False], size=substrate_size,  # Grid of downward linkages
                                        p=[structural_homogeneity, 1 - structural_homogeneity])
        self.layer_linkage = self.r.choice(a=[True, False], size=substrate_size,  # Grid of layer linkages
                                        p=[layer_homogenity, 1 - layer_homogenity])
        self.dysfunctional = self.r.choice(a=[True, False], size=substrate_size,  # Grid of dysfunctional nodes
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter])

        self.inactive = np.zeros(substrate_size, dtype=bool)  # Grid of currently dysfunctional nodes

    def activate_pacemaker(self):
        # Activate the substrate pacemaker cells
        self.activation[:, 0,:] = self.refractory_period

    def iterate(self):
        excited = self.activation == self.refractory_period  # Condition for being excited
        resting = self.activation == 0  # Condition for resting

        excited_from_rear = np.roll(excited, 1, axis=1)
        excited_from_rear[:,0] = np.bool_(False)  # Eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(excited, -1, axis=1)
        excited_from_fwrd[:, -1] = np.bool_(False)

        excited_from_inside = np.roll(excited & self.layer_linkage, 1, axis=2)
        excited_from_inside[:,:,0] = np.bool(False)

        excited_from_outside = np.roll(excited & np.roll(self.layer_linkage, 1, axis=2), -1, axis=2)
        excited_from_outside[:,:,-1] = np.bool(False)

        excited_from_above = np.roll(excited & self.linkage, 1, axis=0)

        excited_from_below = np.roll(excited & np.roll(self.linkage, 1, axis=0), -1, axis=0)

        excitable = (excited_from_rear | excited_from_fwrd | excited_from_above |
                     excited_from_below | excited_from_inside | excited_from_outside)

        self.inactive[self.dysfunctional & excitable] = (np.random.random(len(self.inactive[self.dysfunctional
                                                                                            & excitable]))
                                                         < self.dysfunction_probability
                                                         )
        self.activation[~resting] -= 1  # If not resting, reduce activation count by one
        self.activation[resting & excitable & ~self.inactive] = self.refractory_period
        return self.activation

    def identifier(self):
        return '{},{},{},{},{},{},{}'.format(self.substrate_size, self.structural_heterogeneity,self.dysfunction_parameter,
                                    self.dysfunction_probability, self.refractory_period, self.layer_homogenity,
                                    self.seed)


def simulation(runtime, pacemaker_period, substrate):
    result = np.zeros((runtime,) + substrate.substrate_size, dtype='int8')
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()

        result[t] = substrate.iterate()
    return result


def animate(results, save=False, cross_view=False, cross_pos=-1):
    fig = plt.figure()
    if cross_view:
        gs = gridspec.GridSpec(1, 2, width_ratios=np.shape(results)[-2:])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ims = [[ax1.imshow(frame[:,:,0], animated=True), ax2.imshow(frame[:, cross_pos, :], animated=True)] for frame in results]
    else:
        ims = [[plt.imshow(frame[:,:,0], animated=True)] for frame in results]
    ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
                                    repeat_delay=500)
    if save:
        plt.rcParams['animation.ffmpeg_path'] = "C:/Program Files/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"

        writer = animation.writers['ffmpeg'](fps=30)
        print('SAVING')
        t = time.time()
        ani.save(save, writer)
        print('Saved as {} in {:.1f} seconds'.format(save, time.time()-t))
    plt.show()



