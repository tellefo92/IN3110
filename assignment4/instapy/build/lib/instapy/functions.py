import numpy as np
import cv2
from numba import njit
import os

def python_color2gray(image):
    '''
    Function that takes an image read as a 3-dimensional array, applies
    grayscale weights to each pixel, and returns the full grayscale image
    as a 2-dimensional array.
    '''
    # Set weight values
    red_weight = 0.21
    green_weight = 0.72
    blue_weight = 0.07

    shape = image.shape
    
    # Generate "empty" image of same height and width as input image
    greyscale_image = np.empty(shape[:2])

    for i in range(shape[0]):
        for j in range(shape[1]):

            # Get BGR value of pixel
            pixel = image[i,j]
            blue, green, red = pixel

            # Apply greyscale weights to pixel value
            greyscale_image[i,j] = (blue*blue_weight + green*green_weight + red * red_weight) # No need to divide by 3

    # Convert pixel values to uint8
    greyscale_image = greyscale_image.astype(np.uint8)
    
    return greyscale_image

def python_color2sepia(image, stepless_value=1):
    '''
    Function that takes an image read as a 3-dimensional array, applies
    sepia values (at desired intensity) to each pixel, and returns the full
    sepia image as a 3-dimensional array.
    '''
    shape = image.shape

    # Generate "empty" image with same shape as input image
    _sepia_image = np.empty(shape)

    # Scale factor if any channel value exeeds 255
    scale_down = 1

    # Weight for stepless sepia
    non_sepia_weight = 1 - stepless_value

    # Using matrix to hold sepia weight to eliminate hard coded values
    sepia_matrix = [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]

    for i in range(shape[0]):
        for j in range(shape[1]):

            # Get BGR value of pixel
            pixel = image[i,j]
            blue, green, red = pixel

            # Apply sepia values to pixel
            tr = (sepia_matrix[0][0]*red + sepia_matrix[0][1]*green + sepia_matrix[0][2]*blue) * stepless_value
            tg = (sepia_matrix[1][0]*red + sepia_matrix[1][1]*green + sepia_matrix[1][2]*blue) * stepless_value
            tb = (sepia_matrix[2][0]*red + sepia_matrix[2][1]*green + sepia_matrix[2][2]*blue) * stepless_value

            # Adds stepless sepia weight to color channels
            tr += red * non_sepia_weight
            tg += green * non_sepia_weight
            tb += blue * non_sepia_weight

            # Check if any color channel has value above 255
            if max(tr, tg, tb) > 255:
                if 255/max(tr, tg, tb) < scale_down:
                    # Change scale_down factor
                    scale_down = 255/max(tr, tg, tb)

            _sepia_image[i,j] = np.asarray([tb, tg, tr])

    # Scaling down all pixel values
    # Only if there is a value that exceeds 255, and the scale_down factor is not 1
    if scale_down != 1:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k, color in enumerate(_sepia_image[i,j]):
                    _sepia_image[i,j,k] = color * scale_down

    # Convert pixel values to uint8
    _sepia_image = _sepia_image.astype(np.uint8)

    return _sepia_image

def numpy_color2gray(image):
    '''
    Function that takes an image read as a 3-dimensional array, applies
    grayscale weights to each pixel, and returns the full grayscale image
    as a 2-dimensional array.
    '''
    # Set weight values
    red_weight = 0.21
    green_weight = 0.72
    blue_weight = 0.07

    shape = image.shape

    # Generate "empty" image with same shape as input image
    greyscale_image = np.empty(shape[:2])

    # Applying greyscale weights to pixel values using array slicing
    greyscale_image[:,:] = (image[:,:,0]*blue_weight+image[:,:,1]*green_weight+image[:,:,2]*red_weight) # No need to divide by 3

    # Convert pixel values to uint8
    greyscale_image = greyscale_image.astype(np.uint8)

    return greyscale_image

def numpy_color2sepia(image, stepless_value=1):
    '''
    Function that takes an image read as a 3-dimensional array, applies
    sepia values (at desired intensity) to each pixel, and returns the full
    sepia image as a 3-dimensional array.
    '''
    sepia_matrix = np.asarray([[0.393, 0.769, 0.189], 
                               [0.349, 0.686, 0.168], 
                               [0.272, 0.534, 0.131]])

    # Scale down sepia matrix
    sepia_matrix *= stepless_value

    # Weight for stepless sepia
    non_sepia_weight = 1 - stepless_value

    shape = image.shape

    # Generate "empty" image with same shape as input image
    _sepia_image = np.empty(shape)

    _sepia_image[:,:,:] = np.flip(np.flip(image[:,:,:]) @ np.transpose(sepia_matrix)) + image[:,:,:] * non_sepia_weight

    # Check if any color channel has value above 255
    if np.amax(_sepia_image) > 255:
        scale = 255/np.amax(_sepia_image)
        _sepia_image *= scale

    # Convert pixel values to uint8
    _sepia_image = _sepia_image.astype(np.uint8)

    return _sepia_image

@njit
def numba_color2gray(image):
    '''
    Function that takes an image read as a 3-dimensional array, applies
    grayscale weights to each pixel, and returns the full grayscale image
    as a 2-dimensional array.
    '''    
    red_weight = 0.21
    green_weight = 0.72
    blue_weight = 0.07

    shape = image.shape

    # Generate "empty" image of same height and width as input image
    greyscale_image = np.empty(shape[:2])


    for i in range(shape[0]):
        for j in range(shape[1]):

            # Get BGR values of pixel
            pixel = image[i,j]
            blue, green, red = pixel

            # Apply greyscale weights to pixel values
            greyscale_image[i,j] = (blue*blue_weight + green*green_weight + red * red_weight) # No need to divide by 3

    # Convert pixel values to uint8
    greyscale_image = greyscale_image.astype(np.uint8)

    return greyscale_image

@njit
def numba_color2sepia(image, stepless_value=1):
    '''
    Function that takes an image read as a 3-dimensional array, applies
    sepia values (at desired intensity) to each pixel, and returns the full
    sepia image as a 3-dimensional array.
    ''' 
    shape = image.shape

    # Generate "empty" image with same shape as input image
    _sepia_image = np.empty(shape)

    # Scale factor if any channel value exeeds 255
    scale_down = 1

    # Weight for stepless sepia
    non_sepia_weight = 1 - stepless_value
    
    # Using matrix to hold sepia weight to eliminate hard coded values
    sepia_matrix = [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]


    for i in range(shape[0]):
        for j in range(shape[1]):

            # Get BGR value of pixel
            pixel = image[i,j]
            blue, green, red = pixel

            # Apply sepia values to pixel
            tr = (sepia_matrix[0][0]*red + sepia_matrix[0][1]*green + sepia_matrix[0][2]*blue) * stepless_value
            tg = (sepia_matrix[1][0]*red + sepia_matrix[1][1]*green + sepia_matrix[1][2]*blue) * stepless_value
            tb = (sepia_matrix[2][0]*red + sepia_matrix[2][1]*green + sepia_matrix[2][2]*blue) * stepless_value

            tr += red * non_sepia_weight
            tg += green * non_sepia_weight
            tb += blue * non_sepia_weight
            # Check if any color channel has value above 255
            if max(tr, tg, tb) > 255:
                if 255/max(tr, tg, tb) < scale_down:
                    scale_down = 255/max(tr, tg, tb)

            _sepia_image[i,j] = np.asarray([tb, tg, tr])

    # Scaling down all pixel values
    # Only if there is a value that exceeds 255, and the scale_down factor is not 1
    if scale_down != 1:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k, color in enumerate(_sepia_image[i,j]):
                    _sepia_image[i,j,k] = color * scale_down

    # Convert pixel values to uint8
    _sepia_image = _sepia_image.astype(np.uint8)

    return _sepia_image

def grayscale_image(input_filename, output_filename=None, implementation="numpy", scale=1):
    '''
    Function that takes a file in the folder, reads it into an array, 
    and calls the appropriate function to convert it into grayscale. Returns
    the converted array, and saves the image to some specified location with
    a specified name, if given by the user.

    Input:
        - input_filename: Name of image file
        - output_filename: Filename and directory where image should be saved
        - implementation: Which version of the image conversion function to use.
                          Either python, numpy or numba
        - scale: Scale factor if user wishes to scale up/down the image before
                 conversion
    '''

    # Read image to array
    image = cv2.imread(input_filename)

    # Check that image is not empty
    if image is None:
        raise TypeError (f"{input_filename} is not an image file.")
    
    # Check that scale is an int or float greater than 0
    if not isinstance(scale, (int, float)):
        raise ValueError ("To use the scale greyscale filter, please provide a value greater than 0.")
    if not 0 <= scale:
        raise ValueError ("To use the stepless greyscale filter, please provide a value greater than 0.")

    # Resizing
    if scale != 1:
        image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
    print(image.shape)

    # Choose implementation
    if implementation.lower() == "python":
        converted_image = python_color2gray(image)
    elif implementation.lower() == "numpy":
        converted_image = numpy_color2gray(image)
    elif implementation.lower() == "numba":
        converted_image = numba_color2gray(image)
    else:
        raise NameError ("No such implementation")

    # Save image to specified location with specified name
    # Adding _sepia to image name
    name = input_filename.split(".")[0] + "_greyscale." + input_filename.split(".")[1]

    # Set name of output_filename
    if output_filename == None:
        dst = name

    # Checking if output_filename is a valid path, file or valid filename    
    else:
        if os.path.isfile(output_filename):
            dst = output_filename
        elif os.path.isdir(output_filename):
            dst = os.path.join(output_filename, name)
        elif [output_filename] == output_filename.split("."):
            dst = output_filename + input_filename.split(".")[1]
        else:
            dst = output_filename
    cv2.imwrite(dst, converted_image)

def sepia_image(input_filename, output_filename=None, implementation="numpy", stepless_value=1, scale=1):
    '''
    Function that takes a file in the folder, reads it into an array, 
    and calls the appropriate function to apply sepia effect to it. Returns
    the converted array, and saves the image to some specified location with
    a specified name, if given by the user.

    Input:
        - input_filename: Name of image file
        - output_filename: Filename and directory where image should be saved
        - implementation: Which version of the image conversion function to use.
                          Either python, numpy or numba
        - stepless_value: Intensity of sepia effect. Value between 0-1.
        - scale: Scale factor if user wishes to scale up/down the image before
                 conversion
    '''
    # Read image to array
    image = cv2.imread(input_filename)

    # Check that image is not empty
    if image is None:
        raise TypeError (f"{input_filename} is not an image file.")

    # Check that stepless_value is an int or float between 0-1
    if not isinstance(stepless_value, (int, float)):
        raise ValueError ("To use the stepless sepia filter, please provide a value between 0 and 1.")
    if not 0 <= stepless_value <= 1:
        raise ValueError ("To use the stepless sepia filter, please provide a value between 0 and 1.")

    # Check that scale is an int or float greater than 0
    if not isinstance(scale, (int, float)):
        raise ValueError ("To use the scale sepia filter, please provide a value greater than 0.")
    if not 0 <= scale:
        raise ValueError ("To use the stepless sepia filter, please provide a value greater than 0.")

    # Resizing
    if scale != 1:
        image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

    # Choose implementation
    if implementation.lower() == "python":
        converted_image = python_color2sepia(image, stepless_value=stepless_value)
    elif implementation.lower() == "numpy":
        converted_image = numpy_color2sepia(image, stepless_value=stepless_value)
    elif implementation.lower() == "numba":
        converted_image = numba_color2sepia(image, stepless_value=stepless_value)
    else:
        raise NameError ("No such implementation")

    # Save image to specified location with specified name
    # Adding _sepia to image name
    if stepless_value == 1:    
        name = input_filename.split(".")[0] + "_sepia." + input_filename.split(".")[1]
    else:
        name = input_filename.split(".")[0] + f"_sepia_{stepless_value}." + input_filename.split(".")[1]

    # Set name of output_filename
    if output_filename == None:
        dst = name

    # Checking if output_filename is a valid path, file or valid filename    
    else:
        if os.path.isfile(output_filename):
            dst = output_filename
        elif os.path.isdir(output_filename):
            dst = os.path.join(output_filename, name)
        elif [output_filename] == output_filename.split("."):
            dst = output_filename + input_filename.split(".")[1]
        else:
            dst = output_filename
    cv2.imwrite(dst, converted_image)

    return converted_image
