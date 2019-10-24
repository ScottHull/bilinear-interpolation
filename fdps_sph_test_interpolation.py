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
soundspeed_array = interpolation_df[4]

test_file = "/Users/scotthull/Documents/FDPS_SPH/test2/results.00024_00001_00000.dat"
test_df = pd.read_csv(test_file, sep='\t', header=None)

calculated_density = test_df[9]
calculated_internal_energy = test_df[10]
calculated_pressure = test_df[11]
calculated_soundspeed = test_df[13]


my_interpolated_pressures = []
my_interpolated_soundspeeds = []
random_density = []
random_internal_energy = []
random_pressure = []
random_soundspeed = []
for index in [randint(0, len(calculated_density)) for j in range(0, 1000)]:
    pressure_interp = BilinearInterpolation(density_array=density_array, internal_energy_array=internal_energy_array,
                                  variable_array=pressure_array, density=calculated_density[index],
                                  internal_energy=calculated_internal_energy[index], interpolation_type='nearest neighbors')
    soundspeed_interp = BilinearInterpolation(density_array=density_array, internal_energy_array=internal_energy_array,
                                  variable_array=soundspeed_array, density=calculated_density[index],
                                  internal_energy=calculated_internal_energy[index], interpolation_type='nearest neighbors')
    my_interpolated_pressures.append(pressure_interp.interpolate())
    my_interpolated_soundspeeds.append(soundspeed_interp.interpolate())
    random_density.append(calculated_density[index])
    random_internal_energy.append(calculated_internal_energy[index])
    random_pressure.append(calculated_pressure[index])
    random_soundspeed.append(calculated_soundspeed[index])
df = pd.DataFrame(
    {
        'sph_density': random_density,
        'sph_internal_energy': random_internal_energy,
        'sph_pressure': random_pressure,
        'sph_soundspeed': random_soundspeed,
        'eos_pressure': my_interpolated_pressures,
        'eos_soundspeed': my_interpolated_soundspeeds,
    }
)
df.to_csv('sph_vs_eos_interpolation.csv', sep=" ")

fig = plt.figure()
ax = Axes3D(fig)
ax.plot(density_array, internal_energy_array, pressure_array, color='blue')
ax.scatter(random_density, random_internal_energy, random_pressure, color='red')
ax.scatter(random_density, random_internal_energy, my_interpolated_pressures, color='green')
ax.set_xlabel("Density")
ax.set_ylabel("Internal Energy")
ax.set_zlabel("Pressure")

fig2 = plt.figure()
ax2 = Axes3D(fig2)
ax2.plot(density_array, internal_energy_array, soundspeed_array, color='blue')
ax2.scatter(random_density, random_internal_energy, random_soundspeed, color='red')
ax2.scatter(random_density, random_internal_energy, my_interpolated_soundspeeds, color='green')
ax2.set_xlabel("Density")
ax2.set_ylabel("Internal Energy")
ax2.set_zlabel("Sound Speed")

plt.show()













# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot(density_array, internal_energy_array, soundspeed_array, color='blue')

# for i in [randint(0, len(calculated_density)) for j in range(0, 100)]:
#     b = BilinearInterpolation(density_array=density_array, internal_energy_array=internal_energy_array,
#                               variable_array=soundspeed_array, density=calculated_density[i],
#                               internal_energy=calculated_internal_energy[i], interpolation_type='nearest neighbors')
#
#     ax.scatter(calculated_density[i], calculated_internal_energy[i], b.interpolate(), color='red')
#
# ax.scatter(calculated_density, calculated_internal_energy, calculated_soundspeed, color='green')
#
# ax.set_xlabel("Density")
# ax.set_ylabel("Internal Energy")
# ax.set_zlabel("Sound Speed")

plt.show()
