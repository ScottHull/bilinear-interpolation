import pandas as pd


def restrict_density_indices_to_single_density(density_array, given_density, grid_length=120, bound='lower'):
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
            if i >= given_density:
                b1 = index
                b2 = index + grid_length - 1
                if b2 > len(density_array) - 1:
                    b2 = len(density_array) - 1
                break
    else:
        for index, i in enumerate(reversed(density_array)):
            if i <= given_density:
                b2 = len(density_array) - (index - 1) - grid_length - 1
                b1 = len(density_array) - (index - 1) - (2 * grid_length)
                if b1 < 0:
                    b1 = 0
                break

    return b1, b2


def calc_distance(given, sample):
    """
    A simple function for calculating directional distances between a given value and a sample value.
    :param given:
    :param sample:
    :return:
    """
    distance = given - sample
    return distance


def get_entropy_neighbors(restriced_indices, entropy_array, given_entropy):
    """
    Get the nearest entropy neighbors to a given entropy value in a restricted array.
    :param d1_indices: 
    :param d2_indices: 
    :param entropy_array: 
    :param given_entropy: 
    :return: 
    """
    
    entropy_array_restricted = entropy_array[restriced_indices[0]:restriced_indices[1]]

    min_distance = None
    min_distance_index = None

    for index, i in enumerate(entropy_array_restricted):
        distance = calc_distance(given=given_entropy, sample=i)
        if min_distance is None:
            min_distance = distance
            min_distance_index = index
        elif abs(distance) < abs(min_distance):
            min_distance = distance
            min_distance_index = index
    if min_distance < 0:
        return (min_distance_index - 1, min_distance_index)
    elif min_distance > 0:
        return (min_distance_index, min_distance_index + 1)
    else:
        return (min_distance_index - 1, min_distance_index + 1)


def get_energy_neighbor_values(s11, s12, s21, s22, lower_density_restricted_indices,
                               upper_density_restricted_indices, energy_array):
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
    :param energy_array:
    :return:
    """

    e11 = energy_array[lower_density_restricted_indices[0]:lower_density_restricted_indices[1]][s11]
    e12 = energy_array[lower_density_restricted_indices[0]:lower_density_restricted_indices[1]][s12]
    e21 = energy_array[upper_density_restricted_indices[0]:upper_density_restricted_indices[1]][s21]
    e22 = energy_array[upper_density_restricted_indices[0]:upper_density_restricted_indices[1]][s22]

    return (e11, e12, e21, e22)


def bilinear_interpolate(x1, x2, x, y1, y2, y, q11, q12, q21, q22):
    f1 = (((x2 - x) / (x2 - x1)) * q11) + (((x - x1) / (x2 - x1)) * q21)
    f2 = (((x2 - x) / (x2 - x1)) * q12) + (((x - x1) / (x2 - x1)) * q22)
    f = (((y2 - y) / (y2 - y1)) * f1) + (((y - y1) / (y2 - y1)) * f2)
    return f

def linear_interpolate(x1, x2, x, q1, q2):
    f = (((x2 - x) / (x2 - x1)) * q1) + (((x2 - x) / (x2 - x1)) * q2)
    return f

def interpolate_energy(density_neighbor_values, entropy_neighbor_values, energy_neighbor_values, density, entropy):
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

    # print(p1)
    # print(p2)
    # print(s11)
    # print(s12)
    # print(s21)
    # print(s22)
    # print(u11)
    # print(u12)
    # print(u21)
    # print(u22)
    # print(density)
    # print(entropy)

    u1 = linear_interpolate(x1=s11, x2=s12, x=entropy, q1=u11, q2=u12)
    u2 = linear_interpolate(x1=s21, x2=s22, x=entropy, q1=u21, q2=u22)
    u = linear_interpolate(x1=p1, x2=p2, x=density, q1=u1, q2=u2)

    return u




df = pd.read_fwf("/Users/scotthull/Desktop/bilinear_interpolation/granite.rho_u.txt", header=None)  # load in the granite.rho_u.txt file
density = list(df[0])  # load in the full-length density array from df
energy = list(df[1])  # load in the full-length energy array from df
entropy = list(df[5])  # load in the full-length entropy array from df

given_density = 1.22597792E+03  # pick a plausible value for density to interpolate against
given_entropy = -4.97858159E+03  # pick a plausible value for entropy to interplate against

# now, given that we'll have energy values within a range of a single density in df, we must restrict the density array
# the following 2 functions will return the 'upper' and 'lower' nearest neighbor index ranges to given_density
# we can use these to restrict the arrays to within these index ranges
# d1 indices will give the index range for density which gives the 'lower' nearest neighbor
# d2 indices will give the index range for density which gives the 'upper' nearest neighbor
d1_indices = restrict_density_indices_to_single_density(density_array=density, given_density=given_density, grid_length=120, bound='lower')
d2_indices = restrict_density_indices_to_single_density(density_array=density, given_density=given_density, grid_length=120, bound='upper')

# now, restrict the density array based on d1_indices and d2_indices
density_1_array = density[d1_indices[0]:d1_indices[1]]
density_2_array = density[d2_indices[0]:d2_indices[1]]

# we will restrict the entropy array also based on the index ranges given by d1_indices and d2_indices
# the following 2 functions will return the nearest entropy neighbors to given_entropy with the restricted upper and lower array
lower_entropy_neighbors = get_entropy_neighbors(restriced_indices=d1_indices, entropy_array=entropy, given_entropy=given_entropy)
upper_entropy_neighbors = get_entropy_neighbors(restriced_indices=d2_indices, entropy_array=entropy, given_entropy=given_entropy)

# because we need nearest energy neighbors for interpolation, we get the energy values at the same index location as the entropy values
energy_neighbors = get_energy_neighbor_values(s11=lower_entropy_neighbors[0], s12=lower_entropy_neighbors[1],
                                              s21=upper_entropy_neighbors[0], s22=upper_entropy_neighbors[1],
                                              lower_density_restricted_indices=d1_indices,
                                              upper_density_restricted_indices=d2_indices,
                                              energy_array=energy)

# package the neighbor values up for use for interpolation
density_neighbor_values = (density[d1_indices[0]:d1_indices[1]][0], density[d2_indices[0]:d2_indices[1]][0])
restricted_entropy_array_lower = entropy[d1_indices[0]:d1_indices[1]]
restricted_entropy_array_upper = entropy[d2_indices[0]:d2_indices[1]]
entropy_neighbor_values = (restricted_entropy_array_lower[lower_entropy_neighbors[0]],
                           restricted_entropy_array_lower[lower_entropy_neighbors[1]],
                           restricted_entropy_array_upper[upper_entropy_neighbors[0]],
                           restricted_entropy_array_upper[upper_entropy_neighbors[1]])
energy_neighbor_values = energy_neighbors

# finally, attempt to interpolate energy
energy = interpolate_energy(density_neighbor_values=density_neighbor_values,
                     entropy_neighbor_values=entropy_neighbor_values,
                     energy_neighbor_values=energy_neighbors,
                     density=given_density,
                     entropy=given_entropy)

print(d1_indices, d2_indices)
print(density_neighbor_values)
print(lower_entropy_neighbors, upper_entropy_neighbors)
print(entropy_neighbor_values)
print(energy_neighbor_values)
print(energy)




# def get_bounds(density_array, given_density):
#     """
#     Gets the bounds on 3 values for the purpose of interpolating entropy when given the ordered density array.
#     :param density_array:
#     :param given_density:
#     :return:
#     """
#     lower_bound_value = None
#     upper_bound_value = None  # the first index value that contains a value greater than the target value
#     lower_bound_index = None
#     upper_bound_index = None
#     upper_bound_array = []
#     lower_bound_array = []
#     found_lower_bound = False
#     found_upper_bound = False
#     for index, i in enumerate(density_array):
#         if found_upper_bound is True:
#             if i != upper_bound_value:
#                 upper_bound_index = index - 1
#                 break
#         if i > given_density and upper_bound_value is None:
#             upper_bound_value = i
#             found_upper_bound = True
#         if upper_bound_value is not None and i == upper_bound_value:
#             upper_bound_array.append(i)
#
#     for index, i in enumerate(reversed(density_array)):
#         if found_lower_bound is True:
#             if i != lower_bound_value:
#                 lower_bound_index = len(density_array) - (index - 1)
#                 break
#         if i < given_density and lower_bound_value is None:
#             lower_bound_value = i
#             found_lower_bound = True
#         if lower_bound_value is not None and i == lower_bound_value:
#             lower_bound_array.append(i)
#
#     return lower_bound_index, upper_bound_index
#
# def get_bounds_with_grid_length(density_array, given_density, grid_length):
#     """
#     Gets the bounds on 3 values for the purpose of interpolating entropy when given the ordered density array.
#     :param density_array:
#     :param given_density:
#     :return:
#     """
#     lower_bound_value = None
#     upper_bound_value = None  # the first index value that contains a value greater than the target value
#     lower_bound_index = None
#     upper_bound_index = None
#     upper_bound_array = []
#     lower_bound_array = []
#     found_lower_bound = False
#     found_upper_bound = False
#     for index, i in enumerate(density_array):
#         if i >= given_density and upper_bound_value is None:
#             upper_bound_value = i
#             found_upper_bound = True
#             upper_bound_index = index + grid_length - 1
#             if upper_bound_index > len(density_array) - 1:
#                 upper_bound_index = len(density_array) - 1
#             break
#
#     for index, i in enumerate(reversed(density_array)):
#         if i < given_density and lower_bound_value is None:
#             lower_bound_value = i
#             found_lower_bound = True
#             lower_bound_index = len(density_array) - (index - 1) - grid_length
#             if lower_bound_index < 0:
#                 lower_bound_index = 0
#             break
#
#     return lower_bound_index, upper_bound_index
#
#
# def restrict_density_indices(density_array, given_density):
#     """
#     Assumption: the given array is rank ordered and does not contain duplicates.
#     :param density_array:
#     :param given_density:
#     :return:
#     """
#     b = get_bounds(density_array, given_density)
#
#     return b