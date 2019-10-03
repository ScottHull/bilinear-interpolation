from interpolation import BilinearInterpolation

import pandas as pd

import matplotlib.pyplot as plt


interpolation_file = pd.read_csv('/Users/scotthull/Desktop/FDPS_SPH_ScottHull/eos/granite.rho_u.csv')
original_data_file = pd.read_csv('/Users/scotthull/Desktop/FDPS_SPH_ScottHull/eos/granite.table.csv')

density_array = interpolation_file['Density (kg/m3)']
energy_array = interpolation_file['Energy (J/kg)']
temperature_array = interpolation_file['Temperature (K)']

original_density_array = original_data_file['Density (kg/m3)']
original_energy_array = original_data_file['Energy (J/kg)']
original_temperature_array = original_data_file['Temperature (K)']

test_densities = [0.000001, 2174.9167, 25416.5203]
corresponding_energies = []
corresponding_temperatures = []

for i in test_densities:
    c_e = []
    c_t = []
    for index, j in enumerate(density_array):
        if j == i:
            c_e.append(energy_array[index])
            c_t.append(temperature_array[index])


fig = plt.figure()
ax = fig.add_subplot(111)
for index, i in enumerate(test_densities):
    ax.plot([i for j in corresponding_energies[index]], corresponding_energies[index], linewidth=2.0, label=str(i))
ax.set_xlabel("Density")
ax.set_ylabel("Internal Energy")
ax.legend(loc='lower right')
ax.grid()