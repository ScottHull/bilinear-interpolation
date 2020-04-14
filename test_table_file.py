from interpolation import GenericTrilinearInterpolation, BilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_fwf("dunite.rho_u.txt", header=None)
# df = pd.read_fwf("dunite.rho_u.txt", header=None)

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

# l = len(density)
#
# for index, i in enumerate(df[1]):
#     print("Interpolating: {} / {}".format(index + 1, l))
#     d = df[0][index]
#     s = df[5][index]
#     u = df[1][index]
#     p = df[3][index]
#
#     model = GenericTrilinearInterpolation(var1_array=density, var2_array=energy,
#                                                    var3_array=pressure,
#                                                    var1=d, var2=u, grid_length=120)
#     try:
#         interp = model.interpolate()
#         sample_d.append(d)
#         sample_s.append(s)
#         sample_u.append(u)
#         sample_p.append(p)
#         interpolated_p.append(interp)
#     except:
#         interpolation_errors.append((d, p))
#
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111)
# ax1.scatter(sample_d, sample_p, color='blue', marker="+", label='sample')
# ax1.scatter(sample_d, interpolated_p, color='red', marker="+", label='interpolated')
# ax1.scatter([i[0] for i in interpolation_errors], [i[1] for i in interpolation_errors], color='green', marker="+",
#             label="interpolation error")
# ax1.set_xlabel("density")
# ax1.set_ylabel("pressure")
# ax1.legend(loc='upper left')
# ax1.grid()
#
# plt.show()

d = 3.1206352422255359e+03
s = 3.0000000000000000e+03
u_m = GenericTrilinearInterpolation(var1_array=density, var2_array=entropy, var3_array=energy,
                                               var1=d, var2=s, grid_length=120)
print(u_m.interpolate(), "2.4860989715216281e+06")

d2 = 3.1206352423109220e+03
u = 2.4860990001875977e+06
print(u / u_m.interpolate())
p_m = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=pressure,
                                               var1=d2, var2=u, grid_length=120)
print(p_m.interpolate())
pm_2 = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=pressure,
                                               var1=d2, var2=u_m.interpolate(), grid_length=120)
print(pm_2.interpolate())
