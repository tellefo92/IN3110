import numpy as np
import cv2
from numba import njit
import random
import instapy
from instapy import python_color2gray, python_color2sepia, numpy_color2gray, numpy_color2sepia, numba_color2gray, numba_color2sepia

image = (np.random.standard_normal([50, 50, 3]) * 255).astype(np.uint8)

def test_grayscale():
    '''
    Test that all functions returns the same 2-dimensional array.
    '''
    python_grayscale = python_color2gray(image)
    numpy_grayscale = numpy_color2gray(image)
    numba_grayscale = numba_color2gray(image)
    assert python_grayscale.all() == numpy_grayscale.all() == numba_grayscale.all()

def test_sepia_regular():
    '''
    Test that all functions returns the same 3-dimensional array

    Also tests that a random pixel in all converted images has the same
    channel values as manually applying the weights to a random pixel.
    '''
    python_sepia = python_color2sepia(image)
    numpy_sepia = numpy_color2sepia(image)
    numba_sepia = numba_color2sepia(image)

    i = random.randint(0,50)
    j = random.randint(0,50)

    pixel = image[i,j]
    blue, green, red = pixel

    # Apply sepia values to pixel
    tr = (0.393*red + 0.769*green + 0.189*blue)
    tg = (0.349*red + 0.686*green + 0.168*blue)
    tb = (0.272*red + 0.534*green + 0.131*blue)

    pixel_values = np.asarray([tb, tg, tr])

    assert python_sepia.all() == numpy_sepia.all() == numba_sepia.all()
    assert python_sepia[i,j].all() == numpy_sepia[i,j].all() == numba_sepia[i,j].all() == pixel_values.all()

def test_sepia_stepless():
    '''
    Test that all functions returns the same 3-dimensional array

    Also tests that a random pixel in all converted images has the same
    channel values as manually applying the weights to a random pixel.
    '''
    stepless_value = random.random()
    non_sepia_weight = 1 - stepless_value

    python_sepia = python_color2sepia(image)
    numpy_sepia = numpy_color2sepia(image)
    numba_sepia = numba_color2sepia(image)

    i = random.randint(0,50)
    j = random.randint(0,50)

    pixel = image[i,j]
    blue, green, red = pixel

    # Apply sepia values to pixel
    tr = (0.393*red + 0.769*green + 0.189*blue) * stepless_value
    tg = (0.349*red + 0.686*green + 0.168*blue) * stepless_value
    tb = (0.272*red + 0.534*green + 0.131*blue) * stepless_value

    tr += red * non_sepia_weight
    tg += green * non_sepia_weight
    tb += blue * non_sepia_weight

    pixel_values = np.asarray([tb, tg, tr])

    assert python_sepia.all() == numpy_sepia.all() == numba_sepia.all()
    assert python_sepia[i,j].all() == numpy_sepia[i,j].all() == numba_sepia[i,j].all() == pixel_values.all()
