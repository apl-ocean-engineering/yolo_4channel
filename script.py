#!/usr/bin/env python3
# TODO:
#       - get list of filepaths for every image to be processed
#       - loop through images, send each to function that processes them
#         and returns the result
#       - save result under modified filepath


# list of every filepath
#   - assume script is run at base directory of all images
#       | - script
#       | - image folder 1
#       | - image folder 2
#       | - results (if run before)
#   - user-specified filetype for images (global variable)
#     default = png

import glob
import os

cwd = os.getcwd()
files = glob.glob(cwd + '/**/*.png', recursive=True)
print(files)

def processImage(image):
    # do stuff

    return result
