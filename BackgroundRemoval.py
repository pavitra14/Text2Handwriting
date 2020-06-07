import cv2
import numpy as np

# https://medium.com/better-programming/automating-white-or-any-other-color-background-removal-with-python-and-opencv-4be4addb6c99

def processImage(image):
    output = image
    # Set thresholds. Here, we are using the Hue, Saturation, Value color space model. We will be using these values to decide what values to show in the ranges using a minimum and maximum value. 
    #THESE VALUES CAN BE PLAYED AROUND FOR DIFFERENT COLORS
    hMin = 29  # Hue minimum
    sMin = 30  # Saturation minimum
    vMin = 0   # Value minimum (Also referred to as brightness)
    hMax = 179 # Hue maximum
    sMax = 255 # Saturation maximum
    vMax = 255 # Value maximum
    # Set the minimum and max HSV values to display in the output image using numpys' array function. We need the numpy array since OpenCVs' inRange function will use those.
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    # Create HSV Image and threshold it into the proper range.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Converting color space from BGR to HSV
    mask = cv2.inRange(hsv, lower, upper) # Create a mask based on the lower and upper range, using the new HSV image
    # Create the output image, using the mask created above. This will perform the removal of all unneeded colors, but will keep a black background.
    output = cv2.bitwise_and(image, image, mask=mask)
    # Add an alpha channel, and update the output image variable
    *_, alpha = cv2.split(output)
    dst = cv2.merge((output, alpha))
    output = dst

    # Resize the image
    h, w, _ = image.shape
    dim = (h, 120)
    output = cv2.resize(output, dim)
    
    return output