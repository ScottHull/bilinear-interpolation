from interpolation import BilinearInterpolation
from extrapolation import LinearExtrapolation

import os

from random import randint

import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


extrapolation_path = '/Users/scotthull/PycharmProjects/bilinear_interpolation/granite.table.txt'
experimental_df = pd.read_fwf(extrapolation_path, header=None)
experimental_density_array = experimental_df[0]
experimental_internal_energy_array = experimental_df[2]

extrapolate = LinearExtrapolation(density_array=experimental_density_array,
                                  internal_energy_array=experimental_internal_energy_array)


interpolation_path = '/Users/scotthull/PycharmProjects/bilinear_interpolation/granite.rho_u.txt'
interpolation_df = pd.read_fwf(interpolation_path, header=None)
density_array = interpolation_df[0]
internal_energy_array = interpolation_df[1]
pressure_array = interpolation_df[3]

test_file = "/Users/scotthull/Documents/FDPS_SPH/test2/results.00028_00001_00000.dat"
test_df = pd.read_csv(test_file, sep='\t', header=None)

calculated_density = test_df[9]
calculated_internal_energy = test_df[10]
calculated_pressure = test_df[11]

fig = plt.figure()
ax = Axes3D(fig)
ax.plot(density_array, internal_energy_array, pressure_array, color='blue')

for i in [randint(0, len(calculated_density)) for j in range(0, 100)]:
    b = BilinearInterpolation(density_array=density_array, internal_energy_array=internal_energy_array,
                              variable_array=pressure_array, density=calculated_density[i],
                              internal_energy=calculated_internal_energy[i], interpolation_type='nearest neighbors')

    ax.scatter(calculated_density[i], calculated_internal_energy[i], b.interpolate())

ax.set_xlabel("Density")
ax.set_ylabel("Internal Energy")
ax.set_zlabel("Pressure")

plt.show()
