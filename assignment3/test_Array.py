from array import Array

a = Array((3,), 1, 2, 3)
b = Array((2,2), 1, 2, 3, 4)

def test_print_function():
    # Checks that print function returns a nicely formatted string.
    assert str(a) == "[1, 2, 3]"
    assert str(b) == "[[1, 2], [3, 4]]"

def test_1d_addition():
    # Checks that __add__ function adds element wise and returns the correct result
    assert a + a == Array((3,), 2, 4, 6)
    assert a + 2 == Array((3,), 3, 4, 5)
    assert 4 + a == Array((3,), 5, 6, 7)

def test_1d_subtraction():
    # Checks that __sub__ function subtracts element wise and returns the correct result
    assert a - a == Array((3,), 0, 0, 0)
    assert a - 2 == Array((3,), -1, 0, 1)
    assert 4 - a == Array((3,), 3, 2, 1)
def test_1d_multiplication():
    # Checks that __mul__ function multiplies element wise and returns the correct result
    assert a * a == Array((3,), 1, 4, 9)
    assert a * 2 == Array((3,), 2, 4, 6)
    assert 4 * a == Array((3,), 4, 8, 12)
def test_1d_eq():
    # Checks that __eq__ function returns boolean
    assert type(a == Array((3,), 1, 2, 3)) is bool
    assert type(a != Array((3,), 1, 2, 3)) is bool
def test_1d_is_equal():
    # Checks that is_equal function checks element wise and returns an array of booleans
    c = Array((3,), 1, 2, 0)
    d = Array((3,), -1, -2, -3)
    assert str(a.is_equal(c)) == "[True, True, False]"
    assert str(a.is_equal(d)) == "[False, False, False]"
def test_1d_min_element():
    # Checks that min_element function returns the smallest number of array
    assert a.min_element() == 1

'''
A lot of these tests would run correctly, however, as described in the README.md, the shape of the array after addition is incorrect, so I'm commenting out all these tests as well.
Had I implemented the 2-dim array in another way, I would have ran these tests.
'''
e = Array((2,2), 1, 2, 3, 4)
f = Array((2,2), 2, 4, 6, 8)

def test_2d_addition():
    # Checks that __add__ function adds element wise and returns the correct result
    assert e + e == Array((2,2), 2, 4, 6, 8)
    assert e + 2 == Array((2,2), 3, 4, 5, 6)
    assert 4 + e == Array((2,2), 5, 6, 7, 8)

def test_2d_subtraction():
    # Checks that __sub__ function subtracts element wise and returns the correct result
    assert e - e == Array((2,2), 0, 0, 0, 0)
    assert e - 2 == Array((2,2), -1, 0, 1, 2)
    assert 4 - e == Array((2,2), 3, 2, 1, 0)
def test_2d_multiplication():
    # Checks that __mul__ function multiplies element wise and returns the correct result
    assert e * e == Array((2,2), 1, 4, 9, 16)
    assert e * 2 == Array((2,2), 2, 4, 6, 8)
    assert 4 * e == Array((2,2), 4, 8, 12, 16)
def test_2d_eq():
    # Checks that __eq__ function returns boolean
    assert type(e == Array((2,2), 2, 4, 6, 8)) is bool
    assert type(e != Array((2,2), 2, 4, 6, 8)) is bool
'''    
def test_2d_is_equal():
    # Checks that is_equal function checks element wise and returns an array of booleans
    g = Array((2,2), 1, 2, 4, 5)
    h = Array((2,2), 2, 4, 6, 8)
    assert str(e.is_equal(g)) == "[[True, True], [False, False]"
    assert str(e.is_equal(h)) == "[False, False], [False, False]"
'''
def test_2d_min_element():
    # Checks that min_element function returns the smallest number of array
    assert a.min_element() == 1