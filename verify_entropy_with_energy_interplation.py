from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_fwf("/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/bilinear-interpolation/granite.rho_u.txt", header=None)  # load in the granite.rho_u.txt file

test_file = "/Users/scotthull/Desktop/results.00001_00001_00000.dat"
test_df = pd.read_csv(test_file, sep='\t', header=None)

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
sample_u = []
interpolated_u = []

verify_s = []

# for index, i in enumerate([randint(0, len(density) - 1) for j in range(0, 2000)]):
for index, i in enumerate(test_df[1]):
    id = test_df[1][index]
    d = test_df[9][index]
    u = test_df[10][index]
    s = test_df[13][index]
    #
    # model = GenericTrilinearInterpolation(var1_array=density, var2_array=entropy, var3_array=energy,
    #                             var1=d, var2=3000, grid_length=120)
    # u = model.interpolate()

    if u > 0 and i == 0:
        sample_d.append(d)
        sample_u.append(u)
        interpolated_u.append(u)

        # verify_model = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=entropy,
        #                                              var1=2390.27342, var2=5429700.626766, grid_length=120)
        verify_model = BilinearInterpolation(density_array=density, internal_energy_array=energy, variable_array=entropy,
                                             density=d, internal_energy=u)

        s_ver = verify_model.interpolate()
        sample_s.append(s)
        verify_s.append(s_ver)


fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.scatter(sample_d, verify_s, color='black')
ax2.scatter(sample_u, verify_s, color='black')
ax1.grid()
ax2.grid()
ax1.set_title("Verify Entropy Interpolation")
ax1.set_xlabel("Sample Density")
ax1.set_ylabel("Interpolated Entropy")
ax2.set_xlabel("Sample Energy")
ax2.set_ylabel("Interpolated Entropy")

fig2 = plt.figure()
ax = Axes3D(fig2)
ax.scatter(sample_d, sample_u, verify_s)
ax.set_xlabel("Sample Density")
ax.set_ylabel("Sample Energy")
ax.set_zlabel("Interpolated Entropy")






# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(interpolated_u, sample_s, color='blue', linewidth=2.0, label="Sample S")
# ax.scatter(interpolated_u, verify_s, color='red', linewidth=2.0, label="Verified S")
# ax.set_xlabel("Interpolated U")
# ax.set_ylabel("S")
# ax.set_title("U Interpolation Verification as a Function of S")
# ax.legend(loc='center right')
# ax.grid()
#
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)
# ax2.scatter(interpolated_u, [(x / y) * 100 for x, y in zip(verify_s, sample_s)])
# ax2.set_xlabel("Interpolated U")
# ax2.set_ylabel("Verified S / Sample S * 100")
# ax2.set_title("U Interpolation Verification as a Function of S")
# ax2.grid()
#
# fig3 = plt.figure()
# ax3 = fig3.add_subplot(111)
# n, bins, patches = ax3.hist([(x / y) * 100 for x, y in zip(verify_s, sample_s)], 50, range=(-20, 400))
# ax3.set_xlabel("Verified S / Sample S * 100")
# ax3.set_ylabel("Number")
# ax3.set_title("Histogram for U Interpolation Verification as a Function of S")
# ax3.grid()
#
# fig4 = plt.figure()
# ax4 = fig4.add_subplot(111)
# ax4.scatter(sample_d, [(abs(x - y)) / y for x, y in zip(verify_s, sample_s)])
# ax4.set_xlabel("Sample Density")
# ax4.set_ylabel("abs(s_verified - s_sample) / s_sample")
# ax4.set_title("Verified S Error")
# ax4.grid()

fig5 = plt.figure()
ax5 = fig5.add_subplot(111)
n, bins, patches = ax5.hist([(abs(x - y)) / y for x, y in zip(verify_s, sample_s)], 100, range=(0, 4))
ax5.set_xlabel("abs(s_verified - s_sample) / s_sample")
ax5.set_ylabel("Number")
ax5.set_title("Verified S Error")
ax5.grid()

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.set_xlabel("Density")
# ax.set_ylabel("Entropy")
# ax.set_zlabel("Internal Energy")
#
# ax.plot(density, entropy, energy, color='blue')
#
# errors = {'d': [], 's': [], 'u': []}
# successes = {'d': [], 's': [], 'u': []}
# for index, d in enumerate(sample_d):
#     s = sample_s[index]
#     u = interpolated_u[index]
#
#     ax.scatter(d, s, u, color='red')

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

