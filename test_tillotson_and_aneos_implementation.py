from interpolation import GenericTrilinearInterpolation
import pandas as pd
import matplotlib.pyplot as plt


granite_df = pd.read_fwf("/Users/scotthull/PycharmProjects/bilinear_interpolation/granite.rho_u.txt",
                 header=None)  # load in the granite.rho_u.txt file

iron_df = pd.read_fwf("/Users/scotthull/PycharmProjects/bilinear_interpolation/iron___.rho_u.txt",
                 header=None)  # load in the granite.rho_u.txt file

granite_density = list(granite_df[0])  # load in the full-length density array from df
granite_energy = list(granite_df[1])  # load in the full-length energy array from df
granite_entropy = list(granite_df[5])  # load in the full-length entropy array from df

iron_density = list(iron_df[0])  # load in the full-length density array from df
iron_energy = list(iron_df[1])  # load in the full-length energy array from df
iron_entropy = list(iron_df[5])  # load in the full-length entropy array from df

test_file = "/Users/scotthull/Documents/FDPS_SPH/test2/results.00001_00001_00000.dat"
test_df = pd.read_csv(test_file, sep='\t', header=None)

sample_d = []
sample_s = []
interpolated_u = []
c_interpolated_u = []
verify_s = []
id_list = []

for index, i in enumerate(test_df[1]):
    id = test_df[1][index]
    d = test_df[9][index]
    u = test_df[10][index]
    s = test_df[13][index]
    sample_s_val = 3000
    print(id)

    if id == 0:
        interp_u = GenericTrilinearInterpolation(var1_array=granite_density, var2_array=granite_entropy, var3_array=granite_energy,
                                                 var1=d, var2=sample_s_val, grid_length=120).interpolate()

        interp_s = GenericTrilinearInterpolation(var1_array=granite_density, var2_array=granite_energy, var3_array=granite_entropy,
                                                 var1=d, var2=interp_u, grid_length=120).interpolate()

        id_list.append(id)
        c_interpolated_u.append(u)
        sample_d.append(d)
        sample_s.append(sample_s_val)
        interpolated_u.append(interp_u)
        verify_s.append(interp_s)

    elif id == 1:
        interp_u = GenericTrilinearInterpolation(var1_array=iron_density, var2_array=iron_entropy,
                                                 var3_array=iron_energy,
                                                 var1=d, var2=sample_s_val, grid_length=120).interpolate()

        interp_s = GenericTrilinearInterpolation(var1_array=iron_density, var2_array=iron_energy,
                                                 var3_array=iron_entropy,
                                                 var1=d, var2=interp_u, grid_length=120).interpolate()


        id_list.append(id)
        c_interpolated_u.append(u)
        sample_d.append(d)
        sample_s.append(sample_s_val)
        interpolated_u.append(interp_u)
        verify_s.append(interp_s)


fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
n1, bins1, patches1 = ax1.hist([(abs(x - y)) / y for x, y in zip(verify_s, sample_s)], 100, range=(0, .002))
ax1.set_xlabel("abs(s_verified - s_sample) / s_sample")
ax1.set_ylabel("Number")
ax1.set_title("Verified S Error")
ax1.grid()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
n2, bins2, patches2 = ax2.hist([(abs(x - y)) / y for x, y in zip(c_interpolated_u, interpolated_u)], 100, range=(0, 5))
ax2.set_xlabel("abs(c_interp_u - py_interp_u) / py_sample")
ax2.set_ylabel("Number")
ax2.set_title("Verified U C++ to Python Interpolation Error")
ax2.grid()

plt.show()