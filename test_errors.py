import pandas as pd
from interpolation import GenericTrilinearInterpolation

df = pd.read_fwf("dunite2.rho_u.txt", header=None, skiprows=2)

density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df
tempertaure = list(df[2])
pressure = list(df[3])
soundspeed = list(df[4])


d = 4827.15
s = -9.60775e+71

model = GenericTrilinearInterpolation(var1_array=density, var2_array=energy,
                                                   var3_array=soundspeed,
                                                   var1=d, var2=s, grid_length=80)

print(model.interpolate())