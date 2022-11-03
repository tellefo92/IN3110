
# Assignment 3

### Functionality
A program to create 1 and 2 dimensional arrays without the use of the numpy module.

The array supports elements of type either int, float or boolean, and can be a mix of these. \
If there's a mix, the program will convert all elements to floats.

The program can add, subtract and multiply arrays of same shapes element wise, \
or it can add, subtract and multiply elements of an array with a constant.
Can also compare arrays, both if they are identical as a whole, or check if/which \
elements of the array are identical. The program also supports finding the \
smallest element of an array.

### Missing Functionality
Although 2-dimensional addition, subtraction, multiplication and comparisons are functional, \
because of the way I've structured my program, one of the tests, namely test_is_equal(), does not work correctly. After \
making all "inner" arrays into Array objects, I have not been able to correctly convert the shape. \
This results in 2-d arrays having shape (2,), despite having arrays inside one "outer" array.
\
I tried fixing this, but wouldn't be able to without having to rewrite my entire code.

### Usage
To create an array, simply do 
```python
my_array = Array(shape, *values)
```
where: \
- shape is a tuple, either (n,) for 1-dimensional arrays or (n,m) for 2-dimensional arrays \
and m,n are integers, and
- \*values are of type either int, float or boolean, or a mix of these.

The following functionality is available on an array object:
```python
# Printing the array
print(my_array)
# Accessing certain elements of the array
my_array[0:3]
# Add elements of arrays
my_array + other_array
my_array + 1
3 - my_array
# Subtract elements of arrays
my_array - other_array
my_array - 3
4.5 - my_array
# Multiply elements of arrays
my_array * other_array
my_array * 2
4 * my_array
# Check if two arrays are equal
my_array == other_array
# Check which elements of two arrays are equal
my_array.is_equal(other_array)
# Find the smallest number in an array
my_array.min_element()
```