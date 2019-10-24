import pandas as pd
import matplotlib.pyplot as plt



interpolation_path = '/Users/scotthull/Documents - Scott’s MacBook Pro/Graduate Research/bilinear-interpolation/granite.rho_u.txt'
interpolation_df = pd.read_fwf(interpolation_path, header=None)
density_array = interpolation_df[0]
internal_energy_array = interpolation_df[1]
entropy_array = interpolation_df[5]


sorted_entropies = {}

for index, density in enumerate(density_array):
    entropy = entropy_array[index]
    internal_energy = internal_energy_array[index]

    if not entropy in sorted_entropies.keys():
        sorted_entropies.update({
            entropy: {
                'density': [density],
                'internal_energy': [internal_energy]
            }
        })
    else:
        sorted_entropies[entropy]['density'].append(density)
        sorted_entropies[entropy]['internal_energy'].append(internal_energy)

fig = plt.figure()
ax = fig.add_subplot(111)

for entropy in sorted_entropies.keys():
    density = sorted_entropies[entropy]['density']
    internal_energy = sorted_entropies[entropy]['internal_energy']
    ax.plot(density, internal_energy, linewidth=0.5, label=str(entropy))
ax.grid()
ax.set_xlabel("Density")
ax.set_ylabel("Internal Energy")
ax.set_title("Internal Energy as Function of Density at Constant Entropy (Adiabatic)")

plt.show()