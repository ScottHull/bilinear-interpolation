from interpolation import GenericTrilinearInterpolation
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_fwf(
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/bilinear-interpolation/granite.rho_u.txt",
    header=None)  # load in the granite.rho_u.txt file

density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df

val1 = 2.51998535E+03
val2 = 2.40419893E+03
verify_model = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=entropy,
                                             var1=val1, var2=val2, grid_length=120)
u = verify_model.interpolate()

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(val1, val2, u, color='blue')
ax.scatter(verify_model.var1_neighbors[0], verify_model.var2_neighbors[0], verify_model.var3_neighbors[0], color='red')
ax.scatter(verify_model.var1_neighbors[0], verify_model.var2_neighbors[1], verify_model.var3_neighbors[0], color='red')
ax.scatter(verify_model.var1_neighbors[0], verify_model.var2_neighbors[1], verify_model.var3_neighbors[1], color='red')
ax.scatter(verify_model.var1_neighbors[0], verify_model.var2_neighbors[0], verify_model.var3_neighbors[1], color='red')
ax.scatter(verify_model.var1_neighbors[1], verify_model.var2_neighbors[0], verify_model.var3_neighbors[0], color='red')
ax.scatter(verify_model.var1_neighbors[1], verify_model.var2_neighbors[1], verify_model.var3_neighbors[0], color='red')
ax.scatter(verify_model.var1_neighbors[1], verify_model.var2_neighbors[0], verify_model.var3_neighbors[1], color='red')
ax.scatter(verify_model.var1_neighbors[1], verify_model.var2_neighbors[1], verify_model.var3_neighbors[1], color='red')

ax.set_xlabel("Density")
ax.set_ylabel("Energy")
ax.set_zlabel("Entropy")

plt.show()
