import pandas as pd

from random import randint


class BilinearInterpolation:

    def __init__(self, density_array, internal_energy_array, variable_array, density, internal_energy,
                 interpolation_type="nearest_neighbors", calculated=False):

        self.density_array = density_array
        self.internal_energy_array = internal_energy_array
        self.variable_array = list(variable_array)
        self.density = density
        self.internal_energy = internal_energy

        if not calculated:
            self.variable_matrix = self.matrix_variable()
        if interpolation_type.lower() == 'boundaries':
            self.points = self.getBoundaries()
        else:
            self.points = self.get_nearest_neighbors()


    def matrix_variable(self):

        m = []
        row = []
        count = 0
        density_index = 0
        energy_index = 0
        current_density = None
        for index, i in enumerate(self.density_array):
            if count == 0:
                current_density = i
            if i != current_density:
                current_density = i
                density_index += 1
                energy_index = 0
                m.append(row)
                row = []

            row.append(self.variable_array[count])

            energy_index += 1
            count += 1

        return m

    def getBoundaries(self):

        # density_neighbors = (self.density_array[0], self.density_array[len(self.density_array) - 1])
        # energy_neighbors = (self.internal_energy_array[0], self.internal_energy_array[len(self.internal_energy_array) - 1])
        # corresponding_variables = (self.variable_matrix[0][0], self.variable_matrix[len(self.variable_matrix) - 1][60 - 1])

        density_neighbors = (min(self.density_array), max(self.density_array))
        energy_neighbors = (min(self.internal_energy_array), max(self.internal_energy_array))

        # q11 = (density_neighbors[0], energy_neighbors[0], self.variable_matrix[0][0])
        # q12 = (density_neighbors[1], energy_neighbors[0], self.variable_matrix[len(self.variable_matrix) - 1][0])
        # q21 = (density_neighbors[0], energy_neighbors[1], self.variable_matrix[0][60 - 1])
        # q22 = (density_neighbors[1], energy_neighbors[1], max(self.variable_array))

        variable_neighbors = [0, 0, 0, 0]
        z = zip(self.density_array, self.internal_energy_array, self.variable_array)


        for i in z:
            d = i[0]
            e = i[1]
            v = i[2]
            if d == density_neighbors[0] and e == energy_neighbors[0]:
                variable_neighbors[0] = v
            elif d == density_neighbors[1] and e == energy_neighbors[0]:
                variable_neighbors[1] = v
            elif d == density_neighbors[0] and e == energy_neighbors[1]:
                variable_neighbors[2] = v
            elif d == density_neighbors[1] and e == energy_neighbors[1]:
                variable_neighbors[3] = v
            else:
                pass

        q11 = (density_neighbors[0], energy_neighbors[0], variable_neighbors[0])
        q12 = (density_neighbors[1], energy_neighbors[0], variable_neighbors[1])
        q21 = (density_neighbors[0], energy_neighbors[1], variable_neighbors[2])
        q22 = (density_neighbors[1], energy_neighbors[1], variable_neighbors[3])

        return [q11, q12, q21, q22]


    def get_nearest_neighbors(self):

        z = zip(self.density_array, self.internal_energy_array, self.variable_array)

        def calc_distance(x, y, x1, y1):
            return (((x - x1)**2) + ((y - y1)**2))**(1/2)

        q11 = None
        q21 = None
        q12 = None
        q22 = None


        for i in z:

            d = i[0]
            e = i[1]

            distance = calc_distance(self.density, self.internal_energy, d, e)
            if d < self.density and e < self.internal_energy:
                if q11 is None:
                    q11 = i
                else:
                    q11_distance = calc_distance(self.density, self.internal_energy, q11[0], q11[1])
                    if distance < q11_distance:
                        q11 = i
            elif d > self.density and e < self.internal_energy:
                if q21 is None:
                    q21 = i
                else:
                    q21_distance = calc_distance(self.density, self.internal_energy, q21[0], q21[1])
                    if distance < q21_distance:
                        q21 = i
            elif d < self.density and e > self.internal_energy:
                if q12 is None:
                    q12 = i
                else:
                    q12_distance = calc_distance(self.density, self.internal_energy, q12[0], q12[1])
                    if distance < q12_distance:
                        q12 = i
            elif d > self.density and e > self.internal_energy:
                if q22 is None:
                    q22 = i
                else:
                    q22_distance = calc_distance(self.density, self.internal_energy, q22[0], q22[1])
                    if distance < q22_distance:
                        q22 = i

        if q11 is None and q21 is not None:
            q11 = q21
        elif q11 is not None and q21 is None:
            q21 = q11
        elif q12 is None and q22 is not None:
            q12 = q22
        elif q12 is not None and q22 is None:
            q22 = q12

        return [q11, q21, q12, q22]



    def interpolate(self):

        '''
        Interpolate (x,y) from values associated with four points.
        The four points are a list of four triplets:  (x, y, value).
        The four points can be in any order.  They should form a rectangle.
        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0
        '''

        # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

        points = sorted(self.points)               # order points by x, then by y
        (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

        if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
            raise ValueError('points do not form a rectangle')
        if not x1 <= self.density <= x2 or not y1 <= self.internal_energy <= y2:
            raise ValueError('(x, y) not within the rectangle')

        return (q11 * (x2 - self.density) * (y2 - self.internal_energy) +
                q21 * (self.density - x1) * (y2 - self.internal_energy) +
                q12 * (x2 - self.density) * (self.internal_energy - y1) +
                q22 * (self.density - x1) * (self.internal_energy - y1)
                ) / ((x2 - x1) * (y2 - y1) + 0.0)



class EntropyBilinearInterpolation:

    def __init__(self, density_array, entropy_array, variable_array, density, entropy,
                 interpolation_type):

        self.density_array = density_array
        self.entropy_array = entropy_array
        self.variable_array = list(variable_array)
        self.density = density
        self.entropy = entropy

        self.variable_matrix = self.matrix_variable()
        if interpolation_type.lower() == 'boundaries':
            self.points = self.getBoundaries()
        else:
            self.points = self.get_nearest_neighbors()


    def matrix_variable(self):

        m = []
        row = []
        count = 0
        density_index = 0
        energy_index = 0
        current_density = None
        for index, i in enumerate(self.density_array):
            if count == 0:
                current_density = i
            if i != current_density:
                current_density = i
                density_index += 1
                energy_index = 0
                m.append(row)
                row = []

            row.append(self.variable_array[count])

            energy_index += 1
            count += 1

        return m

    def getBoundaries(self):


        density_neighbors = (min(self.density_array), max(self.density_array))
        entropy_neighbors = (min(self.entropy_array), max(self.entropy_array))

        variable_neighbors = [0, 0, 0, 0]
        z = zip(self.density_array, self.entropy_array, self.variable_array)


        for i in z:
            d = i[0]
            e = i[1]
            v = i[2]
            if d == density_neighbors[0] and e == entropy_neighbors[0]:
                variable_neighbors[0] = v
            elif d == density_neighbors[1] and e == entropy_neighbors[0]:
                variable_neighbors[1] = v
            elif d == density_neighbors[0] and e == entropy_neighbors[1]:
                variable_neighbors[2] = v
            elif d == density_neighbors[1] and e == entropy_neighbors[1]:
                variable_neighbors[3] = v
            else:
                pass

        q11 = (density_neighbors[0], entropy_neighbors[0], variable_neighbors[0])
        q12 = (density_neighbors[1], entropy_neighbors[0], variable_neighbors[1])
        q21 = (density_neighbors[0], entropy_neighbors[1], variable_neighbors[2])
        q22 = (density_neighbors[1], entropy_neighbors[1], variable_neighbors[3])

        return [q11, q12, q21, q22]


    def get_nearest_neighbors(self):

        z = zip(self.density_array, self.entropy_array, self.variable_array)

        def calc_distance(x, y, x1, y1):
            return (((x - x1)**2) + ((y - y1)**2))**(1/2)

        q11 = None
        q21 = None
        q12 = None
        q22 = None


        for i in z:

            d = i[0]
            e = i[1]

            distance = calc_distance(self.density, self.entropy, d, e)
            if d < self.density and e < self.entropy:
                if q11 is None:
                    q11 = i
                else:
                    q11_distance = calc_distance(self.density, self.entropy, q11[0], q11[1])
                    if distance < q11_distance:
                        q11 = i
            elif d > self.density and e < self.entropy:
                if q21 is None:
                    q21 = i
                else:
                    q21_distance = calc_distance(self.density, self.entropy, q21[0], q21[1])
                    if distance < q21_distance:
                        q21 = i
            elif d < self.density and e > self.entropy:
                if q12 is None:
                    q12 = i
                else:
                    q12_distance = calc_distance(self.density, self.entropy, q12[0], q12[1])
                    if distance < q12_distance:
                        q12 = i
            elif d > self.density and e > self.entropy:
                if q22 is None:
                    q22 = i
                else:
                    q22_distance = calc_distance(self.density, self.entropy, q22[0], q22[1])
                    if distance < q22_distance:
                        q22 = i

        if q11 is None and q21 is not None:
            q11 = q21
        elif q11 is not None and q21 is None:
            q21 = q11
        elif q12 is None and q22 is not None:
            q12 = q22
        elif q12 is not None and q22 is None:
            q22 = q12

        return [q11, q21, q12, q22]



    def interpolate(self):

        '''
        Interpolate (x,y) from values associated with four points.
        The four points are a list of four triplets:  (x, y, value).
        The four points can be in any order.  They should form a rectangle.
        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0
        '''

        # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

        points = sorted(self.points)               # order points by x, then by y
        (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

        # if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        #     raise ValueError('points do not form a rectangle')
        # if not x1 <= self.density <= x2 or not y1 <= self.entropy <= y2:
        #     raise ValueError('(x, y) not within the rectangle')

        return (q11 * (x2 - self.density) * (y2 - self.entropy) +
                q21 * (self.density - x1) * (y2 - self.entropy) +
                q12 * (x2 - self.density) * (self.entropy - y1) +
                q22 * (self.density - x1) * (self.entropy - y1)
                ) / ((x2 - x1) * (y2 - y1) + 0.0)



class EnergyInterpolation:

    def __init__(self, density_array, entropy_array, energy_array, density, entropy, grid_length=120):
        self.density = density
        self.entropy = entropy
        self.density_array = density_array
        self.entropy_array = entropy_array
        self.energy_array = energy_array
        self.grid_length = grid_length

    def restrict_density_indices_to_single_density(self, density_array, given_density, bound='lower'):
        """
        Gets the bounds on 3 values for the purpose of interpolating entropy when given the ordered density array.
        :param density_array:
        :param given_density:
        :return:
        """
        b1 = None
        b2 = None

        if not bound == 'lower':
            for index, i in enumerate(density_array):
                if i > given_density:
                    b1 = index
                    b2 = index + self.grid_length
                    if b2 > len(density_array) - 1:
                        b2 = len(density_array) - 1
                    break
        else:
            for index, i in enumerate(reversed(density_array)):
                if i < given_density:
                    # b2 = len(var1_array) - (index - 1) - self.grid_length - 1
                    # b1 = len(var1_array) - (index) - (2 * self.grid_length)
                    b1 = (len(density_array) - 1) - index - (self.grid_length - 1)
                    b2 = b1 + self.grid_length
                    if b1 < 0:
                        b1 = 0
                    if b2 == 0:
                        b2 = self.grid_length
                    break
        if b1 is None and b2 is None:
            b1 = 0
            b2 = self.grid_length
        return b1, b2

    def calc_distance(self, given, sample):
        """
        A simple function for calculating directional distances between a given value and a sample value.
        :param given:
        :param sample:
        :return:
        """
        distance = given - sample
        return distance

    def get_entropy_neighbors(self, restriced_indices):
        """
        Get the nearest entropy neighbors to a given entropy value in a restricted array.
        :param d1_indices:
        :param d2_indices:
        :param self.entropy_array:
        :param self.entropy:
        :return:
        """

        entropy_array_restricted = self.entropy_array[restriced_indices[0]:restriced_indices[1]]

        min_distance = None
        min_distance_index = None

        for index, i in enumerate(entropy_array_restricted):
            distance = self.calc_distance(given=self.entropy, sample=i)
            if min_distance is None:
                min_distance = distance
                min_distance_index = index
            elif abs(distance) < abs(min_distance):
                min_distance = distance
                min_distance_index = index
        if min_distance < 0:
            if min_distance_index <= 0:
                return (min_distance_index, min_distance_index + 1)
            elif min_distance_index + 1 == self.grid_length:
                return (min_distance_index - 2, min_distance_index - 1)
            return (min_distance_index - 1, min_distance_index)
        elif min_distance > 0:
            if min_distance_index + 1 == self.grid_length:
                return (min_distance_index - 2, min_distance_index - 1)
            return (min_distance_index, min_distance_index + 1)
        else:
            if min_distance_index >= self.grid_length - 1:
                return (min_distance_index - 2, min_distance_index - 1)
            elif min_distance_index < 0:
                return (min_distance_index + 1, min_distance_index + 2)
            return (min_distance_index - 1, min_distance_index + 1)

    def get_energy_neighbor_values(self, s11, s12, s21, s22, lower_density_restricted_indices,
                                   upper_density_restricted_indices):
        """
        Get the 4 nearest energy values
        s11: the index position of the lower entropy neighbor at density d1
        s12: the index position of the upper entropy neighbor at density d1
        s21: the index position of the lower entropy neighbor at density d2
        s2: the index position of the upper entropy neighbor at density d2
        :param s11:
        :param s12:
        :param s21:
        :param s22:
        :param self.energy_array:
        :return:
        """

        e11 = self.energy_array[lower_density_restricted_indices[0]:lower_density_restricted_indices[1]][s11]
        e12 = self.energy_array[lower_density_restricted_indices[0]:lower_density_restricted_indices[1]][s12]
        e21 = self.energy_array[upper_density_restricted_indices[0]:upper_density_restricted_indices[1]][s21]
        e22 = self.energy_array[upper_density_restricted_indices[0]:upper_density_restricted_indices[1]][s22]

        return (e11, e12, e21, e22)

    def bilinear_interpolate(self, x1, x2, x, y1, y2, y, q11, q12, q21, q22):
        f1 = (((x2 - x) / (x2 - x1)) * q11) + (((x - x1) / (x2 - x1)) * q21)
        f2 = (((x2 - x) / (x2 - x1)) * q12) + (((x - x1) / (x2 - x1)) * q22)
        f = (((y2 - y) / (y2 - y1)) * f1) + (((y - y1) / (y2 - y1)) * f2)
        return f

    def linear_interpolate(self, x1, x2, x, q1, q2):
        f = (((x2 - x) / (x2 - x1)) * q1) + (((x2 - x) / (x2 - x1)) * q2)
        return f

    def restrict(self):

        # now, given that we'll have energy values within a range of a single density in df, we must restrict the density array
        # the following 2 functions will return the 'upper' and 'lower' nearest neighbor index ranges to given_density
        # we can use these to restrict the arrays to within these index ranges
        # d1 indices will give the index range for density which gives the 'lower' nearest neighbor
        # d2 indices will give the index range for density which gives the 'upper' nearest neighbor
        d1_indices = self.restrict_density_indices_to_single_density(density_array=self.density_array, given_density=self.density,
                                                                bound='lower')
        d2_indices = self.restrict_density_indices_to_single_density(density_array=self.density_array, given_density=self.density,
                                                                bound='upper')

        # now, restrict the density array based on d1_indices and d2_indices
        density_1_array = self.density_array[d1_indices[0]:d1_indices[1]]
        density_2_array = self.density_array[d2_indices[0]:d2_indices[1]]

        # we will restrict the entropy array also based on the index ranges given by d1_indices and d2_indices
        # the following 2 functions will return the nearest entropy neighbors to given_entropy with the restricted upper and lower array
        lower_entropy_neighbors = self.get_entropy_neighbors(restriced_indices=d1_indices)
        upper_entropy_neighbors = self.get_entropy_neighbors(restriced_indices=d2_indices)

        # because we need nearest energy neighbors for interpolation, we get the energy values at the same index location as the entropy values
        energy_neighbors = self.get_energy_neighbor_values(s11=lower_entropy_neighbors[0], s12=lower_entropy_neighbors[1],
                                                      s21=upper_entropy_neighbors[0], s22=upper_entropy_neighbors[1],
                                                      lower_density_restricted_indices=d1_indices,
                                                      upper_density_restricted_indices=d2_indices)

        # package the neighbor values up for use for interpolation
        density_neighbor_values = (self.density_array[d1_indices[0]:d1_indices[1]][0], self.density_array[d2_indices[0]:d2_indices[1]][0])
        restricted_entropy_array_lower = self.entropy_array[d1_indices[0]:d1_indices[1]]
        restricted_entropy_array_upper = self.entropy_array[d2_indices[0]:d2_indices[1]]
        entropy_neighbor_values = (restricted_entropy_array_lower[lower_entropy_neighbors[0]],
                                   restricted_entropy_array_lower[lower_entropy_neighbors[1]],
                                   restricted_entropy_array_upper[upper_entropy_neighbors[0]],
                                   restricted_entropy_array_upper[upper_entropy_neighbors[1]])

        return (density_neighbor_values, entropy_neighbor_values, energy_neighbors)

    def interpolate(self):

        r = self.restrict()

        density_neighbor_values = r[0]
        entropy_neighbor_values = r[1]
        energy_neighbor_values = r[2]

        p1 = density_neighbor_values[0]
        p2 = density_neighbor_values[1]
        s11 = entropy_neighbor_values[0]
        s12 = entropy_neighbor_values[1]
        s21 = entropy_neighbor_values[2]
        s22 = entropy_neighbor_values[3]
        u11 = energy_neighbor_values[0]
        u12 = energy_neighbor_values[1]
        u21 = energy_neighbor_values[2]
        u22 = energy_neighbor_values[3]

        u1 = self.linear_interpolate(x1=s11, x2=s12, x=self.entropy, q1=u11, q2=u12)
        u2 = self.linear_interpolate(x1=s21, x2=s22, x=self.entropy, q1=u21, q2=u22)
        u = self.linear_interpolate(x1=p1, x2=p2, x=self.density, q1=u1, q2=u2)

        return u





class GenericTrilinearInterpolation:

    def __init__(self, var1_array, var2_array, var3_array, var1, var2, grid_length=120):
        self.var1 = var1
        self.var2 = var2
        self.var1_array = var1_array
        self.var2_array = var2_array
        self.var3_array = var3_array
        self.grid_length = grid_length

        self.var1_neighbors = None
        self.var2_neighbors = None
        self.var3_neighbors = None

        self.p1 = None
        self.p2 = None
        self.s11 = None
        self.s12 = None
        self.s21 = None
        self.s22 = None
        self.u11 = None
        self.u12 = None
        self.u21 = None
        self.u22 = None
        self.u1 = None
        self.u2 = None

    def restrict_var1_indices_to_single_var1(self, var1_array, given_var1, bound='lower'):
        """
        Gets the bounds on 3 values for the purpose of interpolating var2 when given the ordered var1 array.
        :param var1_array:
        :param given_var1:
        :return:
        """
        b1 = None
        b2 = None

        if not bound == 'lower':
            for index, i in enumerate(var1_array):
                if i > given_var1:
                    b1 = index
                    b2 = index + self.grid_length
                    if b2 > len(var1_array) - 1:
                        b2 = len(var1_array) - 1
                    break
        else:
            for index, i in enumerate(reversed(var1_array)):
                if i < given_var1:
                    # b2 = len(var1_array) - (index - 1) - self.grid_length - 1
                    # b1 = len(var1_array) - (index) - (2 * self.grid_length)
                    b1 = (len(var1_array) - 1) - index - (self.grid_length - 1)
                    b2 = b1 + self.grid_length
                    if b1 < 0:
                        b1 = 0
                    if b2 == 0:
                        b2 = self.grid_length
                    break
        if b1 is None and b2 is None:
            b1 = 0
            b2 = self.grid_length
        return b1, b2

    def calc_distance(self, given, sample):
        """
        A simple function for calculating directional distances between a given value and a sample value.
        :param given:
        :param sample:
        :return:
        """
        distance = given - sample
        return distance

    def get_var2_neighbors(self, restriced_indices):
        """
        Get the nearest var2 neighbors to a given var2 value in a restricted array.
        :param d1_indices:
        :param d2_indices:
        :param self.var2_array:
        :param self.var2:
        :return:
        """

        var2_array_restricted = self.var2_array[restriced_indices[0]:restriced_indices[1]]

        min_distance = None
        min_distance_index = None

        for index, i in enumerate(var2_array_restricted):
            distance = self.calc_distance(given=self.var2, sample=i)
            if min_distance is None:
                min_distance = distance
                min_distance_index = index
            elif abs(distance) < abs(min_distance):
                min_distance = distance
                min_distance_index = index
        if min_distance < 0:
            if min_distance_index <= 0:
                return (min_distance_index, min_distance_index + 1)
            elif min_distance_index + 1 == self.grid_length:
                return (min_distance_index - 2, min_distance_index - 1)
            return (min_distance_index - 1, min_distance_index)
        elif min_distance > 0:
            if min_distance_index + 1 == self.grid_length:
                return (min_distance_index - 2, min_distance_index - 1)
            return (min_distance_index, min_distance_index + 1)
        else:
            if min_distance_index >= self.grid_length - 1:
                return (min_distance_index - 2, min_distance_index - 1)
            elif min_distance_index < 0:
                return (min_distance_index + 1, min_distance_index + 2)
            return (min_distance_index, min_distance_index + 1)

    def get_var3_neighbor_values(self, s11, s12, s21, s22, lower_var1_restricted_indices,
                                   upper_var1_restricted_indices):
        """
        Get the 4 nearest var3 values
        s11: the index position of the lower var2 neighbor at var1 d1
        s12: the index position of the upper var2 neighbor at var1 d1
        s21: the index position of the lower var2 neighbor at var1 d2
        s2: the index position of the upper var2 neighbor at var1 d2
        :param s11:
        :param s12:
        :param s21:
        :param s22:
        :param self.var3_array:
        :return:
        """

        e11 = self.var3_array[lower_var1_restricted_indices[0]:lower_var1_restricted_indices[1]][s11]
        e12 = self.var3_array[lower_var1_restricted_indices[0]:lower_var1_restricted_indices[1]][s12]
        e21 = self.var3_array[upper_var1_restricted_indices[0]:upper_var1_restricted_indices[1]][s21]
        e22 = self.var3_array[upper_var1_restricted_indices[0]:upper_var1_restricted_indices[1]][s22]

        return (e11, e12, e21, e22)

    def bilinear_interpolate(self, x1, x2, x, y1, y2, y, q11, q12, q21, q22):
        f = (q11 * (x2 - self.var1) * (y2 - self.var2) +
                q21 * (self.var1 - x1) * (y2 - self.var2) +
                q12 * (x2 - self.var1) * (self.var2 - y1) +
                q22 * (self.var1 - x1) * (self.var2 - y1)
                ) / ((x2 - x1) * (y2 - y1) + 0.0)
        return f

    def linear_interpolate(self, x1, x2, x, q1, q2):
        f = (((x2 - x) / (x2 - x1)) * q1) + (((x - x1) / (x2 - x1)) * q2)
        return f

    def restrict(self):

        # now, given that we'll have var3 values within a range of a single var1 in df, we must restrict the var1 array
        # the following 2 functions will return the 'upper' and 'lower' nearest neighbor index ranges to given_var1
        # we can use these to restrict the arrays to within these index ranges
        # d1 indices will give the index range for var1 which gives the 'lower' nearest neighbor
        # d2 indices will give the index range for var1 which gives the 'upper' nearest neighbor
        d1_indices = self.restrict_var1_indices_to_single_var1(var1_array=self.var1_array, given_var1=self.var1,
                                                                bound='lower')
        d2_indices = self.restrict_var1_indices_to_single_var1(var1_array=self.var1_array, given_var1=self.var1,
                                                                bound='upper')

        # now, restrict the var1 array based on d1_indices and d2_indices
        var1_1_array = self.var1_array[d1_indices[0]:d1_indices[1]]
        var1_2_array = self.var1_array[d2_indices[0]:d2_indices[1]]

        # we will restrict the var2 array also based on the index ranges given by d1_indices and d2_indices
        # the following 2 functions will return the nearest var2 neighbors to given_var2 with the restricted upper and lower array
        lower_var2_neighbors = self.get_var2_neighbors(restriced_indices=d1_indices)
        upper_var2_neighbors = self.get_var2_neighbors(restriced_indices=d2_indices)

        # because we need nearest var3 neighbors for interpolation, we get the var3 values at the same index location as the var2 values
        var3_neighbors = self.get_var3_neighbor_values(s11=lower_var2_neighbors[0], s12=lower_var2_neighbors[1],
                                                      s21=upper_var2_neighbors[0], s22=upper_var2_neighbors[1],
                                                      lower_var1_restricted_indices=d1_indices,
                                                      upper_var1_restricted_indices=d2_indices)

        # package the neighbor values up for use for interpolation
        var1_neighbor_values = (self.var1_array[d1_indices[0]:d1_indices[1]][0], self.var1_array[d2_indices[0]:d2_indices[1]][0])
        restricted_var2_array_lower = self.var2_array[d1_indices[0]:d1_indices[1]]
        restricted_var2_array_upper = self.var2_array[d2_indices[0]:d2_indices[1]]
        var2_neighbor_values = (restricted_var2_array_lower[lower_var2_neighbors[0]],
                                   restricted_var2_array_lower[lower_var2_neighbors[1]],
                                   restricted_var2_array_upper[upper_var2_neighbors[0]],
                                   restricted_var2_array_upper[upper_var2_neighbors[1]])



        return (var1_neighbor_values, var2_neighbor_values, var3_neighbors)

    def interpolate(self):

        r = self.restrict()

        var1_neighbor_values = r[0]
        var2_neighbor_values = r[1]
        var3_neighbor_values = r[2]

        self.var1_neighbors = var1_neighbor_values
        self.var2_neighbors = var2_neighbor_values
        self.var3_neighbors = var3_neighbor_values

        self.p1 = var1_neighbor_values[0]
        self.p2 = var1_neighbor_values[1]
        self.s11 = var2_neighbor_values[0]
        self.s12 = var2_neighbor_values[1]
        self.s21 = var2_neighbor_values[2]
        self.s22 = var2_neighbor_values[3]
        self.u11 = var3_neighbor_values[0]
        self.u12 = var3_neighbor_values[1]
        self.u21 = var3_neighbor_values[2]
        self.u22 = var3_neighbor_values[3]

        if self.s11 == self.s12:
            self.u1 = self.u11
        else:
            self.u1 = self.linear_interpolate(x1=self.s11, x2=self.s12, x=self.var2, q1=self.u11, q2=self.u12)
        if self.s21 == self.s22:
            self.u2 = self.u21
        else:
            self.u2 = self.linear_interpolate(x1=self.s21, x2=self.s22, x=self.var2, q1=self.u21, q2=self.u22)
        if self.p1 == self.p2:
            u = self.u1
        else:
            u = self.linear_interpolate(x1=self.p1, x2=self.p2, x=self.var1, q1=self.u1, q2=self.u2)


        # print("***************")
        # print(self.var1)
        # print(self.var2)
        # print(self.u1, self.u2)
        # print("var1 neighbors: {}".format(var1_neighbor_values))
        # print("var2 neighbors: {}".format(var2_neighbor_values))
        # print("var3 neighbors: {}".format(var3_neighbor_values))
        # print(u)

        return u