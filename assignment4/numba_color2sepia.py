import cv2
import numpy as np
import random
import time
import sys
from numba import njit
import os

@njit
def convert_image(image, stepless_value):
    '''
    Function that takes a colorized image and applies a sepia filter to it

    Input:
        - image: 3-dimensional array of BGR values
        - stepless_value: The effect of sepia filter on the image (0%-100%)

    Output:
        - 3-dimensional array of BGR values
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

def generate_report(image, stepless_value, input_filename):
    '''
    Function to create a report of average runtime of convert_image function

    Input:
        - image: 3-dimensional array of BGR-values
        - stepless_value: Intensity of sepia filter
        - inputfilename

    Output:
        - Generates a .txt file which contains information about runtime and image
    '''
    with open("numba_report_color2sepia.txt", "w") as outfile:
        script_name = "numba_color2sepia"
        outfile.write(f"Timing: {script_name}\n")
                    
        # Timing
        tot_time = 0
        for i in range(3):
            tic = time.perf_counter()
            _sepia_image = convert_image(image, stepless_value)
            toc = time.perf_counter()
            tot_time += (toc-tic)
        
        # Writing to report
        avg_time = tot_time/3
        outfile.write(f"Average runtime running {script_name} after 3 runs: {avg_time:.6f} s\n")
        other_reports = ["python_report_color2sepia.txt", "numpy_report_color2sepia.txt"]
        for report in other_reports:
            infile = open(report, "r").readlines()
            infile_script_name = infile[0].split()[-1]
            infile_time = float(infile[1].split()[-2])
            comp = "faster" if avg_time < infile_time else "slower"
            comp_time = infile_time/avg_time if comp == "faster" else avg_time/infile_time
            outfile.write(f"Average runtime running {script_name} is {comp_time:.1f} times {comp} than {infile_script_name}.\n")
        image_shape = image.shape
        outfile.write(f"Timing performed using: {input_filename}, size: {image_shape[0]}x{image_shape[1]}")

def sepia_image(input_filename, output_filename=None, stepless_value=1):
    '''
    Function that takes an image file as an input, loads it to an array,
    and calls the function to apply sepia filter to the image. 

    inputs:
        - input_filename: Name of image file
        - output_filename: Set to None by default, can be changed by the user,
        either as name of a directory, the full path to a file, or just some
        name the user wants.
        - stepless_value: Set to 1 by default. Can take values between 0-1, and
        dictates the intensity of the sepia filter on the image.

    Raises:
        - TypeError: If input_filename is not a readable image

    Output:
        - Saves the image with the applied sepia filter to file
    '''

    # Check that stepless_value is an int or float between 0-1
    if not isinstance(stepless_value, (int, float)):
        raise ValueError ("To use the stepless sepia filter, please provide a value between 0 and 1.")
    if not 0 <= stepless_value <= 1:
        raise ValueError ("To use the stepless sepia filter, please provide a value between 0 and 1.")

    # Convert stepless value to float
    stepless_value = float(stepless_value)

    # Read image into array of BGR values
    image = cv2.imread(input_filename)

    # Check that image is not empty
    if image is None:
        raise TypeError (f"{input_filename} is not an image file.")

    # Adding _sepias to image name
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

    # Converting image to sepias        
    _sepia_image = convert_image(image, stepless_value)

    # Generate report
    # generate_report(image, input_filename)

    # Saving sepias image to destination path
    cv2.imwrite(dst, _sepia_image)

if __name__ == "__main__":
    sepia_image("rain.jpg")