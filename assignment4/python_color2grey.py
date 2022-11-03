import cv2
import numpy as np
import random
import time
import sys
import os

def convert_image(image):
    '''
    Function that takes a colorized image converts it into greyscale.

    Input:
    	- image: 3-dimensional array of BGR values

    Returns:
    	- 2-dimensional array of greyscale values
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
    
def generate_report(image, input_filename):
    '''
    Function to create a report of average runtime of convert_image function

    Input:
        - image: 3-dimensional array of BGR-values
        - input_filename

    Output:
        - Generates a .txt file which contains information about runtime and image
    '''
    # Creating report
    with open("python_report_color2grey.txt", "w") as outfile:
        script_name = "python_color2grey"
        outfile.write(f"Timing: {script_name}\n")
                    
        # Timing
        tot_time = 0
        for i in range(3):
            tic = time.perf_counter()
            gimage = convert_image(image)
            toc = time.perf_counter()
            tot_time += (toc-tic)
        
        # Writing to report
        avg_time = tot_time/3
        outfile.write(f"Average runtime running {script_name} after 3 runs: {avg_time:.6f} s\n")
        image_shape = image.shape
        outfile.write(f"Timing performed using: {input_filename}, size: {image_shape[0]}x{image_shape[1]}")

def greyscale_filter(input_filename, output_filename=None):
    '''
    Function that takes an image file as an input, loads it to an array,
    and calls the function to apply grayscale filter to the image. 

    inputs:
        - input_filename: Name of image file
        - output_filename: Set to None by default, can be changed by the user,
        either as name of a directory, the full path to a file, or just some
        name the user wants.

    Raises:
        - TypeError: If input_filename is not a readable image

    Output:
        - Saves the image with the applied grayscale filter to file
    '''

    # Read image into array of BGR values
    image = cv2.imread(input_filename)

    # Check that image is not empty
    if image is None:
        raise TypeError (f"{input_filename} is not an image file.")

    # Adding _greyscale to image name    
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
            dst = output_filename + "." + input_filename.split(".")[1]
        else:
            dst = output_filename

    # Converting image to greyscale        
    greyscale_image = convert_image(image)

    # Generate report
    #generate_report(image, input_filename)

    # Saving greyscale image to destination path
    cv2.imwrite(dst, greyscale_image)

if __name__ == "__main__":
    greyscale_filter("rain.jpg")