class Array:

    def __init__(self, shape, *values):
        '''
        
        Initialize an array of 1 or 2 dimensions. Elements can only be of type:
        - int
        - float
        - bool
        
        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.

        If elements in *values are of different types, all elements are converted to floats.    

        Raises:
            ValueError: If the number of values does not fit with the shape.
        '''
        # Support for 2-dimensional array
        if isinstance(shape, tuple) and len(shape) == 2:
            self.shape = shape
            n = self.shape[0]
            m = self.shape[1]
            # Check if number of values fits with the shape
            #print(values)
            try:
                if n*m != len(values):
                    raise ValueError
            except ValueError:
                print("ValueError: Shape of array does not match number of arguements!")
                print(f"Can't make instance of array with shape {shape} and {len(values)} arguements.")
                exit()
            new = []
            count = 0
            # Check if values are of same type
            m_types = False
            first_value_type = type(values[0])
            for value in values:
                if not isinstance(value, first_value_type):
                    m_types = True
                    break
            # Assigning values to inner arrays
            for i in range(n):
                new2 = []
                for j in range(m):
                    new2.append(float(values[count]) if m_types is True else values[count])
                    count += 1
                new.append(Array((len(new2),), new2))
            self.array = Array((len(new),), new)
        else:
        # Support for 1-dimensional array
            if isinstance(values[0], list):
                values = values[0]
            else:
                values = [x for x in values]
            self.shape = shape
            n = int(str(shape)[1])
            # Check if number of values fits with the shape
            try:
                if n != len(values):
                    raise ValueError
            except ValueError:
                print("ValueError: Shape of array does not match number of arguements!")
                print(f"Can't make instance of array with shape {shape} and {len(values)} arguements.")
                exit()
            # Check if values are of the same type
            first_value_type = type(values[0])
            m_types = False
            for value in values[1:]:
                if not isinstance(value, first_value_type):
                    m_types = True
                    break
            self.array = values if m_types is False else [float(x) for x in values]

    def __str__(self):
        """Returns a nicely printable string representation of the array.
        Returns:
            str: A string representation of the array.
        """
        if isinstance(self.array[0], Array):
            return str([eval(str(self.array[i])) for i in range(len(self.array))])
        else:
            return str(self.array)

    def __getitem__(self, item):
        """ Returns value of item in array .
        Args:
            item (int): Index of value to return .
        Returns:
            value: Value of the given item .
        """
        return self.array[item]

    def __len__(self):
        ''' Returns rows of 1-dimensional array, or number of collumns of 2-dimensional array.
        Returns:
            int: An integer representation of numbers of rows in 1-dimensional array, or
            int: An integer representation of number of collumns of a 2-dimensional array.
        '''
        return len(self.array)


    def __add__(self, other):
        """Element-wise adds Array with another Array or number.
        Calls the __radd__ function if self is not an array
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """
        new = []
        if isinstance(other, (int, float)): # Check if other is an int or float value
            for i in range(len(self.array)):
                new.append(self.array[i] + other)
        elif self.shape == other.shape:
            for i in range(len(self.array)):
                new.append(self.array[i] + other[i])
        return Array((len(new),), new)

    def __radd__(self, other):
        """Function is called if self is an int or float.
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.
        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.
        Returns:
            Array: the difference as a new array.
        """
        new = []
        if isinstance(other, (int, float)): # Check if other is an int or float value
            for i in range(len(self.array)):
                new.append(self.array[i] - other)
        elif len(self.array) == len(other):
            for i in range(len(self.array)):
                new.append(self.array[i] - other[i])
        return Array((len(new),), new)

    def __rsub__(self, other):
        """Function is called if self is an int or float.
        Args:
            other (Array, float, int): The array or number being subtracted from.
        Returns:
            Array: the difference as a new array.
        """
        return (-1*self.__sub__(other))

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.
        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.
        Returns:
            Array: a new array with every element multiplied with `other`.
        """
        new = []
        if isinstance(other, (int, float)): # Check if other is an int or float value
            for i in range(len(self.array)):
                new.append(self.array[i] * other)
        elif len(self.array) == len(other):
            for i in range(len(self.array)):
                new.append(self.array[i] * other[i])
        return Array((len(new),), new)

    def __rmul__(self, other):
        """Function is called if self is an int or float
        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.
        Returns:
            Array: a new array with every element multiplied with `other`.
        """
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.
        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.
        Args:
            other (Array): The array to compare with this array.
        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.
        """
        if not isinstance(other, Array):
            return False
        elif len(self.array) != len(other):
            return False
        else:
            for a,b in zip(self.array, other):
                if a != b:
                    return False
            return True

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.
        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.
        Args:
            other (Array, float, int): The array or number to compare with this array.
        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.
        Raises:
            ValueError: if the shape of self and other are not equal.
        """
        if isinstance(self.array[0], Array):
            new = []
            for i in range(len(self.array)):
                new.append(self.array[i].is_equal(other))
            return Array((len(new),), new)
        else:
            new = []
            if isinstance(other, Array):
                try:
                    if self.shape != other.shape:
                        raise ValueError
                    for a,b in zip(self.array, other):
                        if a == b:
                            new.append(True)
                        else:
                            new.append(False)
                except ValueError:
                    print(f"ValueError: Arrays with shapes {self.shape} and {other.shape} are not equal.")
                    exit()
            else:
                try:
                    if not isinstance(other, (int, float)):
                        raise TypeError
                    for i in range(len(self.array)):
                        if self.array[i] == other:
                            new.append(True)
                        else:
                            new.append(False)
                except TypeError:
                    print(f"TypeError: {repr(other)} is not an array nor number.")
                    exit()
            return Array((len(new),), new)
            

    

    def min_element(self):
        """Returns the smallest value of the array.
        Only needs to work for type int and float (not boolean).
        Returns:
            float: The value of the smallest element in the array.
        """
        if isinstance(self.array[0], Array):
            return min((min(self.array[i])) for i in range(len(self.array)))
        else:
            return float(min(self.array))