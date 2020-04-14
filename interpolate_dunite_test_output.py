from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
from math import sqrt
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


df = pd.read_fwf("dunite3.rho_u.txt", header=None)  # load in the granite.rho_u.txt file

test_file = "/Users/scotthull/Downloads/results.00772_00001_00000.dat"
test_df = pd.read_csv(test_file, sep='\t', header=None, skiprows=2)

density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df
temperature = list(df[2])

particle_id = test_df[1]
x = test_df[3]
y = test_df[4]
z = test_df[5]

sample_radius = []
sample_d = []
sample_s = []
sample_u = []
interpolated_u = []

verify_s = []

for index, i in enumerate(test_df[1]):
    id = test_df[1][index]
    d = test_df[9][index]
    u = test_df[10][index]
    s = test_df[13][index]
    t = test_df[14][index]

    if i != 1:
        r = sqrt(x[index] ** 2 + y[index] ** 2 + z[index] ** 2)
        sample_radius.append(r)
        sample_d.append(d)
        sample_u.append(u)
        interpolated_u.append(u)

        verify_model_s = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=entropy,
                                                       var1=d, var2=u, grid_length=120)

        s_ver = verify_model_s.interpolate()

        sample_s.append(s)
        verify_s.append(s_ver)

s_interpolation_error = [(abs(x - y)) / y for x, y in zip(verify_s, sample_s)]

fig = plt.figure()
ax = fig.add_subplot(111)
n, bins, patches = ax.hist(s_interpolation_error, 100)
ax.set_xlabel("abs(S_interp - S_sample) / S_sample")
ax.set_ylabel("Number")
ax.set_title("S Re-Interpolation Error (Dunite2)")
ax.grid()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(
    [sample_radius[index] for index, i in enumerate(s_interpolation_error) if i <= 0.01],
    [verify_s[index] for index, i in enumerate(s_interpolation_error) if i <= 0.01],
    marker="+", color='aqua', label="Error <= 0.01"
)
ax2.scatter(
    [sample_radius[index] for index, i in enumerate(s_interpolation_error) if 0.01 < i <= 0.05],
    [verify_s[index] for index, i in enumerate(s_interpolation_error) if 0.01 < i <= 0.05],
    marker="+", color='blue', label="0.01 < Error <= 0.05"
)
ax2.scatter(
    [sample_radius[index] for index, i in enumerate(s_interpolation_error) if 0.05 < i <= 0.50],
    [verify_s[index] for index, i in enumerate(s_interpolation_error) if 0.05 < i <= 0.50],
    marker="+", color='green', label="0.05 < Error <= 0.50"
)
ax2.scatter(
    [sample_radius[index] for index, i in enumerate(s_interpolation_error) if i > 0.50],
    [verify_s[index] for index, i in enumerate(s_interpolation_error) if i > 0.50],
    marker="+", color='red', label="Error > 0.50"
)
ax2.set_xlabel("Radius")
ax2.set_ylabel("S_interp")
ax2.set_title("S Re-Interpolation (Dunite2) (Colored to Reflect Error to Sample S)")
ax2.legend(loc='lower right')
ax2.grid()




plt.show()
