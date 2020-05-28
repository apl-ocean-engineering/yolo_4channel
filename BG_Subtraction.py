#!/usr/bin/env python3

# TODO:
#   - try out different methods of background subtraction
#       - current: Mixture of Gaussians
#           - constantly update background model throughout all pictures
#           - reset background ever N number of frames (since the camera is moving)
#       - visualize how they can be used to clean up images
#           - subtract the background in order to have just the cinderblock in the picture

# nabbed from https://docs.opencv.org/master/d1/dc5/tutorial_background_subtraction.html

from __future__ import print_function
from ProcessImageDirectory import *
import cv2 as cv
import ProcessImageDirectory

backSub = cv.createBackgroundSubtractorMOG2()
# backSub = cv.createBackgroundSubtractorKNN()


files = getFilePathList()

for frame in files:
    fgMask = backSub.apply(frame)

    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
