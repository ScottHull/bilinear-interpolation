from interpolation import BilinearInterpolation



class LinearExtrapolation:

    def __init__(self, density_array, internal_energy_array):

        self.density_array = density_array
        self.internal_energy_array = internal_energy_array

    def extrapolate(self, density):

        z = zip(self.density_array, self.internal_energy_array)
        density_sorted = sorted(z, key=lambda tup: tup[0])
        k = density_sorted[-1]
        k_minus_1 = density_sorted[-2]
        x_k = k[0]
        x_k_minus_1 = k_minus_1[0]
        y_k = k[1]
        y_k_minus_1 = k_minus_1[1]

        y = y_k_minus_1 + (((density - x_k_minus_1) / (x_k - k_minus_1)) * (y_k - y_k_minus_1))

        return y

    def extrapolate_then_interpolate(self, density, density_array, internal_energy_array, variable_array, interpolation_type='nearest neighbors'):

        internal_energy = self.extrapolate(density=density)
        b = BilinearInterpolation(density_array=density_array, internal_energy_array=internal_energy_array,
                              variable_array=variable_array, density=density,
                              internal_energy=internal_energy, interpolation_type=interpolation_type)




