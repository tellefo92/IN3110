# Instapy

### Installation
To install the instapy module, run the following command:
```python
pip install .
```

### Functionality
Command-line program to manipulate image files, either by applying a grayscale filter
or adding a sepia effect to the image.

### Usage
To use the program, type following (outside the instapy folder)
```python
instapy -h
```
If you get the error message
```bash
bash: instapy: command not found...
```
you have to type in the following command
```bash
export PATH=$PATH:~/.local/bin
```
Required flags when converting an image are the following:
```
-f FILE, --file FILE: Name of image file or path to image file
-i IMPLEMENTATION, --implement IMPLEMENTATION: Which implementation to use. Choose between python, numpy or numba
and either
-g, --gray: Applying grayscale filter to image
or
-se, --sepia: Applying sepia filter to image
```
Optional flags when converting an image are the following:
```
-sv VALUE, --stepless VALUE: Intensity of sepia effect on image. Must be a float between 0-1.
-sc SCALE, --scale SCALE: Scale factor to resize image. Must be float greater than 0
-o PATH, --out PATH: Path to outfile
-R, --runtime: Calculates average runtime of image conversion over 3 runs.
```