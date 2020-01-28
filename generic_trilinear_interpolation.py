from interpolation import GenericTrilinearInterpolation
import pandas as pd

df = pd.read_fwf("/Users/scotthull/PycharmProjects/bilinear_interpolation/granite.rho_u.txt",
                 header=None)  # load in the granite.rho_u.txt file
density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df

d = 3.9411361688227453e+03
s = 3000.0

model = GenericTrilinearInterpolation(var1_array=density, var2_array=entropy, var3_array=energy,
                                      var1=d, var2=s, grid_length=120)
u = model.interpolate()

verify_s = GenericTrilinearInterpolation(var1_array=density, var2_array=energy, var3_array=entropy,
                                      var1=d, var2=u, grid_length=120).interpolate()

print(
    "p1: {}\n"
    "p2: {}\n"
    "s11: {}\n"
    "s12: {}\n"
    "s21: {}\n"
    "s22: {}\n"
    "u11: {}\n"
    "u12: {}\n"
    "u21: {}\n"
    "u22: {}\n".format(model.p1, model.p2, model.s11, model.s12, model.s21, model.s22, model.u11, model.u12,
                       model.u21, model.u22)
)

print(u, verify_s)
