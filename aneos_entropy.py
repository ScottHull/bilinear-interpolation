import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from scipy.interpolate import interp1d
from scipy import interpolate

# ----- A user has to change these three parameters  ----------------

inputfilename = "granite.table.txt"  # input ANEOS file. This follows the format from iSALE
outputfilename = "granite.rho_u.txt"  # output ANEOS file
nu = 120  # number of the grid for the internal energy (exponential)


# -------------------------------------------------------------------

# This function is to correct the original ANEOS format that does not include "E"
# This seems to  occur when the exponent reaches -101
def reformat(number):
    if number.find('E') == -1:
        exponent = "-101"
        mantissa = number.split(exponent)
        return float(mantissa[0]) * 10 ** float(exponent)
    else:
        mantissa, exponent = number.split('E')

    return float(mantissa) * 10 ** float(exponent)


aneosfile = [line.split() for line in open(inputfilename)]

temperature = np.zeros(shape=(0, 0))
density = np.zeros(shape=(0, 0))

for i in range(1, len(aneosfile)):
    try:
        temperature = np.append(temperature, reformat(aneosfile[i][1]))
    except IndexError:
        nt = i - 1
        break

for i in range(1, len(aneosfile), nt + 1):
    density = np.append(density, reformat(aneosfile[i][0]))

nr = len(density)  # density grid number

energy = np.zeros(shape=(nr, nt))  # J/kg
pressure = np.zeros(shape=(nr, nt))  # Pa
soundspeed = np.zeros(shape=(nr, nt))  # m/s
entropy = np.zeros(shape=(nr, nt))  # J/kg/K

new_energy = np.zeros(shape=(nr,nu))

i = 1
for m in range(0, nr):
    for n in range(0, nt):
        f_internal_energy = interpolate.interp2d(density, entropy[m], energy[m], kind='linear', fill_value='extrapolate')
        new_energy[m] = f_internal_energy(density[m], entropy[m])

print(new_energy)




