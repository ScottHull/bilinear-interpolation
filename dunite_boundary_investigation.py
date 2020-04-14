from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt


# df = pd.read_fwf("dunite.rho_u.txt", header=None)
df = pd.read_fwf("dunite2.rho_u.txt", header=None)
density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df
pressure = list(df[3])

individual_densities = []
lowest_energies = []
lowest_entropies = []
lowest_pressures = []

used_d = []
used_e = []
used_s = []
used_p = []

for row in df.index:
    d = df[0][row]  # load in the full-length density array from df
    e = df[1][row]  # load in the full-length energy array from df
    s = df[5][row]  # load in the full-length entropy array from df
    p = df[3][row]

    if d not in individual_densities:
        individual_densities.append(d)
        lowest_entropies.append(s)
        lowest_energies.append(e)
        lowest_pressures.append(p)

interpolated_pressure = []
failed_densities = []
for index, i in enumerate(individual_densities):
    try:
        interp = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=pressure,
                                                       var1=i, var2=lowest_energies[index], grid_length=120)
        interpolated_pressure.append(interp.interpolate() * 10**-9)
        used_d.append(i)
        used_e.append(lowest_energies[index])
        used_s.append(lowest_entropies[index])
        used_p.append((lowest_pressures[index]) * 10**-9)
    except:
        failed_densities.append(i)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(used_d, used_p, color='red', marker='+', label='Sample')
ax.scatter(used_d, interpolated_pressure, color='blue', marker='+', label='Interpolated')
ax.set_xlabel("Density")
ax.set_ylabel("Pressure (GPa)")
# ax.set_yscale('log')
ax.set_title("Lowest Energy As Input (dunite_rho_u.txt)")
ax.legend(loc='upper left')
ax.grid()

used_d2 = []
used_e2 = []
used_s2 = []
used_p2 = []

interpolated_pressure2 = []
failed_densities2 = []
failed_pressures2 = []
for index, i in enumerate(individual_densities):
    if i < 9000:
        try:
            interp = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=pressure,
                                                           var1=i, var2=lowest_energies[index] - (lowest_energies[index] * 0.10), grid_length=120)
            interpolated_pressure2.append(interp.interpolate() * 10**-9)
            used_d2.append(i)
            used_e2.append(lowest_energies[index])
            used_s2.append(lowest_entropies[index])
            used_p2.append((lowest_pressures[index]) * 10**-9)
        except:
            failed_densities2.append(i)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(used_d2, used_p2, color='red', marker='+', label='Sample')
ax2.scatter(used_d2, interpolated_pressure2, color='blue', marker='+', label='Interpolated')
ax2.set_xlabel("Density")
ax2.set_ylabel("Pressure (GPa)")
# ax2.set_yscale('log')
# ax2.set_ylim(-10, 10)
ax2.set_title("Lowest Energy - 10% As Input (dunite_rho_u.txt)")
ax2.legend(loc='upper left')
ax2.grid()

plt.show()
