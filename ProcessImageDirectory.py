#!/usr/bin/env python3
# COPY THIS SCRIPT TO THE BASE FOLDER CONTAINING ALL IMAGES / IMAGE FOLDERS

import glob
import os
import cv2
import numpy

FILE_TYPE = ".png"
IMAGE_DIR = "/home/tanner/Cinderblock/images"
# cwd = IMAGE_DIR
cwd = os.getcwd()
backSub = None

# TODO:
# copy over .json files (from labelme) into resulting "processed" directory 
# enable command line input to specify processing technique
# convert script to process each directory separately
#   seems like running MOG on all images resulted in bad data being generated

def processImage_Disparity(image):
    # need to process one directory at a time
    # idea is that each image will have a 4th channel of the differences between it and the previous image
    # therefore first image in directory will have nothing in the 4th channel
    return result


def processImage_Canny(image):
    edges = cv2.Canny(image,100,200)
    edges = edges.astype('uint8')
    result = numpy.dstack((image, edges))
    return result

def processImage_MOG(image):
    global backSub
    if backSub is None:
        backSub = cv2.createBackgroundSubtractorMOG2()

    fgMask = backSub.apply(image)
    print("FGMASK SHAPE: " + str(fgMask.shape))
    cv2.imshow('Frame', image)
    cv2.imshow('FG Mask', fgMask)
    fgMask = fgMask.astype('uint8')
    cv2.waitKey(10)
    result = numpy.dstack((image, fgMask))
    return result

def getAllFilePathList():
    init_files = glob.glob(cwd + '/**/*' + FILE_TYPE, recursive=True)
    files = []
    for path in init_files:
        if "result" in path:
            pass
        else:
            files.append(os.path.relpath(path))
    print(files)
    return files

if __name__ == "__main__":
    files = getAllFilePathList()

    if not os.path.exists('processed'):
        os.mkdir('processed')

    for image in files:
        cur_image = cv2.imread(image)
        fname = os.path.basename(image)
        # print(fname)
        result_image = processImage_MOG(cur_image)
        result_path = cwd + "/processed/" + image
        dir_path = result_path[:-len(fname)]
        print(dir_path)
        print
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok = True)

        cv2.imwrite(result_path, result_image)
