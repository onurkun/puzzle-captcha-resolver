import numpy as np
import argparse
import cv2
import os
import string
import random
from os import listdir
from os.path import isfile, join, splitext
import time
import sys
import math
import base64
from PIL import Image
import io
import warnings
warnings.simplefilter("ignore", DeprecationWarning)




def detect(frame, temp, w, h):

    result = cv2.matchTemplate(frame, temp, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return (max_val, top_left, bottom_right)


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return np.fromstring(imgdata, dtype='uint8')

def build(encoded_image, encoded_partial_image):

    # load the image b64
    full_image = stringToImage(encoded_image)

    ## partial_image
    partial_image = stringToImage(encoded_partial_image)


    image_test = cv2.imdecode(full_image,cv2.IMREAD_COLOR)
    image2 = cv2.resize(image_test, (404, 150) , interpolation = cv2.INTER_AREA)


    image = cv2.bitwise_not(image2)

    # define the list of boundaries
    boundaries = [
        ([80, 80, 70], [130, 120, 120]),
    ]


    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)


    output_new_first = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    output_new_first = cv2.bitwise_not(output_new_first)

    output_new = np.zeros_like(output)
    output_new[:,:,0] = output_new_first
    output_new[:,:,1] = output_new_first
    output_new[:,:,2] = output_new_first




    template_width2 = cv2.imdecode(partial_image,cv2.IMREAD_GRAYSCALE)
    template_width = cv2.resize(template_width2, (83, 55) , interpolation = cv2.INTER_AREA)

    test_22 = cv2.imdecode(partial_image,cv2.IMREAD_COLOR)
    test = cv2.resize(test_22, (83, 55) , interpolation = cv2.INTER_AREA)

    boundaries = [
        ([255, 255, 255], [255, 255, 255]),

    ]

    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")


        mask = cv2.inRange(test, lower, upper)
        template = cv2.bitwise_and(test, test, mask = mask)
        template = cv2.bitwise_not(template)




    tW, tH = template_width.shape[::-1]
    result = detect(output_new, template, tW, tH)
    if result[0] > 0.5:
     cv2.rectangle(image, *result[1:], (0, 255, 0), 2)
     # orta hesap
     buyukNokta = result[2]
     kucukNokta = result[1]
     #ortaX = kucukNokta[0] + math.ceil((buyukNokta[0] - kucukNokta[0]) / 2)
     #ortaY = kucukNokta[1] + math.ceil((buyukNokta[1] - kucukNokta[1]) / 2)
     ortaX = kucukNokta[0]
     ortaY = kucukNokta[1]


    return (ortaX,ortaY)

