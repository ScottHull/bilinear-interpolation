import pandas as pd

from random import randint


class BilinearInterpolation:

    def __init__(self, density_array, internal_energy_array, variable_array, density, internal_energy,
                 interpolation_type):

        self.density_array = density_array
        self.internal_energy_array = internal_energy_array
        self.variable_array = list(variable_array)
        self.density = density
        self.internal_energy = internal_energy

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





