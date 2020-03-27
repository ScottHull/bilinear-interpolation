from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dunite_df = pd.read_fwf("/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/bilinear-interpolation/dunite.rho_u.txt",
                 header=None)
granite_df = pd.read_fwf("/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/bilinear-interpolation/granite.rho_u.txt",
                 header=None)
iron_df = pd.read_fwf("/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/bilinear-interpolation/granite.rho_u.txt",
                 header=None)

dunite_test_file = "/Users/scotthull/Downloads/dunite_results.00100_00001_00000.dat"
dunite_test_df = pd.read_csv(dunite_test_file, sep='\t', header=None)

granite_test_file = "/Users/scotthull/Downloads/granite_results.00100_00001_00000.dat"
granite_test_df = pd.read_csv(granite_test_file, sep='\t', header=None)

dunite_density = list(dunite_df[0])  # load in the full-length density array from df
dunite_energy = list(dunite_df[1])  # load in the full-length energy array from df
dunite_entropy = list(dunite_df[5])  # load in the full-length entropy array from df

granite_density = list(granite_df[0])  # load in the full-length density array from df
granite_energy = list(granite_df[1])  # load in the full-length energy array from df
granite_entropy = list(granite_df[5])  # load in the full-length entropy array from df

iron_density = list(iron_df[0])  # load in the full-length density array from df
iron_energy = list(iron_df[1])  # load in the full-length energy array from df
iron_entropy = list(iron_df[5])  # load in the full-length entropy array from df

dunite_sample_d = []
dunite_sample_s = []
dunite_sample_u = []
dunite_sample_p = []
dunite_interpolated_u = []

dunite_verify_s = []

granite_sample_d = []
granite_sample_s = []
granite_sample_u = []
granite_sample_p = []
granite_interpolated_u = []

granite_verify_s = []

error_pairs_dunite = []
error_pairs_granite = []
dunite_err_list = []
ok_pairs_dunite = []
ok_pairs_granite = []
granite_err_list = []

for index, i in enumerate(dunite_test_df[1]):
    id = dunite_test_df[1][index]
    d = dunite_test_df[9][index]
    u = dunite_test_df[10][index]
    s = dunite_test_df[13][index]
    p = dunite_test_df[11][index]

    if id < 1:

        dunite_sample_d.append(d)
        dunite_sample_u.append(u)
        dunite_sample_p.append(p)
        dunite_interpolated_u.append(u)

        verify_model_s = GenericTrilinearInterpolation(var1_array=dunite_density, var2_array=dunite_energy, var3_array=dunite_entropy,
                                                       var1=d, var2=u, grid_length=120)

        s_ver = verify_model_s.interpolate()

        dunite_sample_s.append(s)
        dunite_verify_s.append(s_ver)

        err = abs(s_ver - s) / s
        dunite_err_list.append(err)

        if err > 0.05:
            error_pairs_dunite.append((d, u))
        else:
            ok_pairs_dunite.append((d, u))
    
for index, i in enumerate(granite_test_df[1]):
    id = granite_test_df[1][index]
    d = granite_test_df[9][index]
    u = granite_test_df[10][index]
    s = granite_test_df[13][index]
    p = granite_test_df[11][index]

    if id < 1:
        granite_sample_d.append(d)
        granite_sample_u.append(u)
        granite_sample_p.append(p)
        granite_interpolated_u.append(u)

        verify_model_s = GenericTrilinearInterpolation(var1_array=granite_density, var2_array=granite_energy, var3_array=granite_entropy,
                                                       var1=d, var2=u, grid_length=120)

        s_ver = verify_model_s.interpolate()

        granite_sample_s.append(s)
        granite_verify_s.append(s_ver)

        err = abs(s_ver - s) / s
        granite_err_list.append(err)

        if err > 0.05:
            error_pairs_granite.append((d, u))
        else:
            ok_pairs_granite.append((d, u))


fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dunite_sample_d, dunite_verify_s, color='red', label='python')
ax.scatter(dunite_sample_d, dunite_sample_s, color='blue', label='c++')
ax.set_xlabel("density")
ax.set_ylabel("entropy")
ax.set_title("dunite")
ax.legend(loc='lower right')
ax.grid()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(granite_sample_d, granite_verify_s, color='red', label='python')
ax2.scatter(granite_sample_d, granite_sample_s, color='blue', label='c++')
ax2.set_xlabel("density")
ax2.set_ylabel("entropy")
ax2.set_title("granite")
ax2.legend(loc='lower right')
ax2.grid()

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.scatter([i[0] for i in error_pairs_dunite], [i[1] for i in error_pairs_dunite], color='red', marker="+", label='>0.05')
ax3.scatter([i[0] for i in ok_pairs_dunite], [i[1] for i in ok_pairs_dunite], alpha=0.6, color='blue', marker="+", label='<=0.05')
ax3.set_xlabel("density")
ax3.set_ylabel("energy")
ax3.set_title("dunite (error > 0.05)")
ax3.legend(loc='upper left')
ax3.grid()

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.scatter([i[0] for i in error_pairs_granite], [i[1] for i in error_pairs_granite], color='red', marker="+", label='>0.05')
ax4.scatter([i[0] for i in ok_pairs_granite], [i[1] for i in ok_pairs_granite], alpha=0.6, color='blue', marker="+", label='<=0.05')
ax4.set_xlabel("density")
ax4.set_ylabel("energy")
ax4.set_title("granite (error > 0.05)")
ax4.legend(loc='upper left')
ax4.grid()



fig5 = plt.figure()
ax5 = fig5.add_subplot(111)
granite_n5, granite_bins5, granite_patches5 = ax5.hist([(abs(x - y)) / y for x, y in zip(granite_verify_s, granite_sample_s)], 100, color='red', alpha=0.8, label="granite")
dunite_n5, dunite_bins5, dunite_patches5 = ax5.hist([(abs(x - y)) / y for x, y in zip(dunite_verify_s, dunite_sample_s)], 100, color='blue', alpha=0.8, label="dunite")
ax5.set_xlabel("abs(s_verified - s_sample) / s_sample")
ax5.set_ylabel("Number")
ax5.set_title("Verified S Error")
ax5.legend(loc='upper right')
ax5.grid()

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.scatter(dunite_sample_d, dunite_err_list, color='black', marker="+")
ax4.set_xlabel("density")
ax4.set_ylabel("entropy error (python - c++ / c++)")
ax4.set_title("dunite")
ax4.legend(loc='upper left')
ax4.grid()

fig6 = plt.figure()
ax6 = fig6.add_subplot(111)
ax6.scatter(dunite_sample_d, dunite_sample_p, marker="+", color='blue', label='dunite')
ax6.scatter(granite_sample_d, granite_sample_p, marker="+", color='red', label='granite')
ax6.set_xlabel("density")
ax6.set_ylabel("pressure")
ax6.legend(loc='upper left')
ax6.grid()


plt.show()
