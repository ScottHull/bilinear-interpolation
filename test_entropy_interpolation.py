from interpolation import EntropyBilinearInterpolation

import os

from random import randint

import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


interpolation_path = '/Users/scotthull/Documents - Scott’s MacBook Pro/Graduate Research/bilinear-interpolation/granite.rho_u.txt'
interpolation_df = pd.read_fwf(interpolation_path, header=None)
density_array = interpolation_df[0]
internal_energy_array = interpolation_df[1]
entropy_array = interpolation_df[5]


fig = plt.figure()
ax = Axes3D(fig)
ax.plot(density_array, entropy_array, internal_energy_array, color='blue')

for i in [randint(0, len(density_array)) for j in range(0, 1)]:
    density = 50
    entropy = 0 * 10**7
    b = EntropyBilinearInterpolation(density=density, entropy=entropy, density_array=density_array,
                                     entropy_array=entropy_array, variable_array=internal_energy_array,
                                     interpolation_type='nearest neighbors')

    ax.scatter(density, entropy, b.interpolate(), color='red')

ax.set_xlabel("Density")
ax.set_ylabel("Entropy")
ax.set_zlabel("Internal Energy")

plt.show()
