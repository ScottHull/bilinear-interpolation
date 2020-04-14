from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# df = pd.read_fwf("granite.rho_u.txt", header=None)
# df = pd.read_fwf("dunite.rho_u.txt", header=None)
df = pd.read_fwf("dunite3.rho_u.txt", header=None)

density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df
pressure = list(df[3])

sample_d = []
sample_s = []
sample_u = []
sample_p = []
interpolated_p = []
interpolation_errors = []

l = len(density)

for index, i in enumerate(df[1]):
    print("Interpolating: {} / {}".format(index + 1, l))
    d = df[0][index]
    s = df[5][index]
    u = df[1][index]
    p = df[3][index]

    model = GenericTrilinearInterpolation(var1_array=density, var2_array=energy,
                                                   var3_array=pressure,
                                                   var1=d, var2=u, grid_length=120)
    try:
        interp = model.interpolate()
        sample_d.append(d)
        sample_s.append(s)
        sample_u.append(u)
        sample_p.append(p)
        interpolated_p.append(interp)
    except:
        interpolation_errors.append((d, p))

print("Number successes: {}\nNumber Errors: {}".format(len(interpolated_p), len(interpolation_errors)))
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(sample_d, sample_p, color='blue', marker="+", label='sample')
ax1.scatter(sample_d, interpolated_p, color='red', marker="+", label='interpolated')
ax1.scatter([i[0] for i in interpolation_errors], [i[1] for i in interpolation_errors], color='green', marker="+",
            label="interpolation error")
ax1.set_xlabel("density")
ax1.set_ylabel("pressure")
ax1.legend(loc='upper left')
ax1.grid()

errors = [abs((x - y) / y) for x, y in zip(interpolated_p, sample_p)]
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
n, bins, patches = ax2.hist(errors, 100, range=(-1, 1))
ax2.set_xlabel("Interpolated P / Sample P * 100")
ax2.set_ylabel("Number")
ax2.grid()

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.scatter([sample_d[index] for index, i in enumerate(errors) if abs(i) < 0.02], [sample_p[index] for index, i in enumerate(errors) if abs(i) < 0.02], color='aqua', marker="+",
            label="Error < 0.02")
ax3.scatter([sample_d[index] for index, i in enumerate(errors) if 0.02 <= abs(i) < 0.05], [sample_p[index] for index, i in enumerate(errors) if 0.02 <= abs(i) < 0.05], color='blue', marker="+",
            label="0.02 <= Error < 0.05")
ax3.scatter([sample_d[index] for index, i in enumerate(errors) if 0.05 <= abs(i) < 0.50], [sample_p[index] for index, i in enumerate(errors) if 0.05 <= abs(i) < 0.50], color='green', marker="+",
            label="0.05 <= Error < 0.50")
ax3.scatter([sample_d[index] for index, i in enumerate(errors) if abs(i) >= 0.50], [sample_p[index] for index, i in enumerate(errors) if abs(i) >= 0.50], color='red', marker="+",
            label="Error > 0.50")
ax3.set_xlabel("density")
ax3.set_ylabel("pressure")
ax3.legend(loc='upper left')
ax3.grid()

plt.show()
