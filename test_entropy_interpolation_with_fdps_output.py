from interpolation import BilinearInterpolation
from extrapolation import LinearExtrapolation

import os

from random import randint

import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D




interpolation_path = '/Users/scotthull/PycharmProjects/bilinear_interpolation/granite.rho_u.txt'
interpolation_df = pd.read_fwf(interpolation_path, header=None)
density_array = interpolation_df[0]
internal_energy_array = interpolation_df[1]
pressure_array = interpolation_df[3]
soundspeed_array = interpolation_df[4]
entropy_array = interpolation_df[5]

test_file = "/Users/scotthull/Documents/FDPS_SPH/test2/results.00100_00001_00000.dat"
test_df = pd.read_csv(test_file, sep='\t', header=None)

calculated_density = test_df[9]
calculated_internal_energy = test_df[10]


my_interpolated_entropy = []
random_density = []
random_internal_energy = []
current_val = 0
num_samples = 1000
for index in [randint(0, len(calculated_density)) for j in range(0, num_samples)]:
    print("{} / {}".format(current_val, num_samples))
    current_val += 1
    density = calculated_density[index]
    internal_energy = calculated_internal_energy[index]
    random_density.append(density)
    random_internal_energy.append(internal_energy)
    entropy_interp = BilinearInterpolation(density_array=calculated_density,
                                           internal_energy_array=calculated_internal_energy,
                                           variable_array=entropy_array,
                                           density=density,
                                           internal_energy=internal_energy,
                                           interpolation_type='nearest neighbors',
                                           calculated=True)
    my_interpolated_entropy.append(entropy_interp.interpolate())

fig = plt.figure()
ax = Axes3D(fig)
ax.plot(density_array, internal_energy_array, entropy_array, color='blue')
ax.scatter(random_density, random_internal_energy, my_interpolated_entropy, color='red')
ax.set_xlabel("Density")
ax.set_ylabel("Internal Energy")
ax.set_zlabel("Entropy")


plt.show()
