from interpolation import EnergyInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_fwf("/Users/scotthull/Desktop/bilinear_interpolation/granite.rho_u.txt", header=None)  # load in the granite.rho_u.txt file

density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df
#
# given_density = 3891.25945254  # pick a plausible value for density to interpolate against
# given_entropy = 300  # pick a plausible value for entropy to interplate against
#
# model = EnergyInterpolation(density_array=density, entropy_array=entropy, energy_array=energy, density=given_density,
#                             entropy=given_entropy, grid_length=120)
# u = model.interpolate()
# print(u)

sample_d = []
sample_s = []
interpolated_u = []

for index, i in enumerate([randint(0, len(density) - 1) for j in range(0, 2000)]):
    d = density[i]
    s = entropy[i]

    model = EnergyInterpolation(density_array=density, entropy_array=entropy, energy_array=energy,
                                density=d, entropy=s, grid_length=120)
    u = model.interpolate()

    sample_d.append(d)
    sample_s.append(s)
    interpolated_u.append(u)

fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlabel("Density")
ax.set_ylabel("Entropy")
ax.set_zlabel("Internal Energy")

ax.plot(density, entropy, energy, color='blue')

errors = {'d': [], 's': [], 'u': []}
successes = {'d': [], 's': [], 'u': []}
for index, d in enumerate(sample_d):
    s = sample_s[index]
    u = interpolated_u[index]

    ax.scatter(d, s, u, color='red')

    # if u < 0:
    #     errors['d'].append(d)
    #     errors['s'].append(s)
    #     errors['u'].append(u)
    # else:
    #     successes['d'].append(d)
    #     successes['s'].append(s)
    #     successes['u'].append(u)

# pd.DataFrame(errors).to_csv('errors_energy_interpolation.csv')
# pd.DataFrame(successes).to_csv('successes_energy_interpolation.csv')
plt.show()

