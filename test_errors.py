import pandas as pd
from interpolation import GenericTrilinearInterpolation

df = pd.read_fwf("duniteS2.rho_u.txt", header=None, skiprows=2)

density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df
pressure = list(df[3])


d = 7.130261246e1
s = 5.407516528e3

model = GenericTrilinearInterpolation(var1_array=density, var2_array=entropy,
                                                   var3_array=pressure,
                                                   var1=d, var2=s, grid_length=120)

print(model.interpolate())