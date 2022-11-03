def _1dim(self, shape, *values):
    if isinstance(values[0], list):
        values = values[0]
    else:
        values = [x for x in values]

    if isinstance(shape, int):
        n = shape
    else:
        n = int(str(shape)[1])

    try:
        if n != len(values):
            raise ValueError
    except ValueError:
        print("ValueError: Shape of array does not match number of arguements!")
        print(f"Can't make instance of array with shape {shape} and {len(values)} arguements.")
        exit()
    first_value_type = type(values[0])
    m_types = False                             # Boolean for multiple types in array
    for value in values[1:]:                    # Check if values are of homogenous type
        if not isinstance(value, first_value_type):
            m_types = True
            break
    return values if m_types is False else [float(x) for x in values]

"""
((3,2,1), 1, 2, 3, 4, 5, 6):
new = []
i = 0:
    kall ndim(2, [1,2])
        j = 0:
            kall 1dim(1, 1)
                returner [1]
        j = 1:
            kall 1dim(1, 2)
                returner [2]
    fjern [1,2] fra values
    legg til [[1], [2]] i new
i = 1:
    kall ndim(2, [3, 4])
        j = 0:
            kall 1dim(1, 3)
                returner [1]
        ...
"""


def _ndim(self, shape, *values):
    """
    inputs:
        shape - list, converted from tuple
        values - list
    returns:
        array of arrays
    """
    new = []
    n = shape[0]
    if len(shape) > 2:
        shape.remove(shape[0])
        for i in range(n)
            new_vals = values[:shape[0]]
            for j in range(len(new_vals)):
                values.remove[0]
            new.append(_ndim(shape, new_vals))


    elif len(shape) == 2:
        count = 0
        for i in range(n):
            new2 = []
            for j in range(shape[1]):
                new2.append(values[count])
                count += 1
            new.append(_1dim(len(new2), new))



    else:
        new.append(_1dim(shape, values))

    return Array(len(new), new)
