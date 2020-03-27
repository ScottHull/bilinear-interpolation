from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dunite_df = pd.read_fwf("/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/bilinear-interpolation/dunite.rho_u.txt",
                 header=None)
dunite_test_file = "/Users/scotthull/Downloads/dunite2_results.00100_00001_00000.dat"
dunite_test_df = pd.read_csv(dunite_test_file, sep='\t', header=None)

dunite_density = list(dunite_df[0])  # load in the full-length density array from df
dunite_energy = list(dunite_df[1])  # load in the full-length energy array from df
dunite_entropy = list(dunite_df[5])  # load in the full-length entropy array from df
dunite_pressure = list(dunite_df[3])

dunite_sample_d = []
dunite_sample_u = []
dunite_sample_p = []
dunite_interpolated_p = []

l = len(dunite_density)


for index, i in enumerate(dunite_test_df[1]):
    id = dunite_test_df[1][index]
    d = dunite_test_df[9][index]
    u = dunite_test_df[10][index]
    s = dunite_test_df[13][index]
    p = dunite_test_df[11][index]

    if id < 1:
        # interp_p = BilinearInterpolation(density_array=dunite_density, internal_energy_array=dunite_energy,
        #                                  variable_array=dunite_pressure, density=d, internal_energy=u)
        interp_p = GenericTrilinearInterpolation(var1_array=dunite_density, var2_array=dunite_energy, var3_array=dunite_pressure,
                                                           var1=d, var2=u, grid_length=120)
        dunite_interpolated_p.append(interp_p.interpolate())
        dunite_sample_d.append(d)
        dunite_sample_u.append(u)
        dunite_sample_p.append(p)


fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(dunite_sample_d, dunite_sample_p, color='blue', marker="+", label='sample')
ax1.scatter(dunite_sample_d, dunite_interpolated_p, color='red', marker="+", label='interpolated')
ax1.set_xlabel("density")
ax1.set_ylabel("pressure")
ax1.set_title("dunite")
ax1.legend(loc='upper left')
ax1.grid()

plt.show()
