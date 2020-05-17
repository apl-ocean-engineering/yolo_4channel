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
import cv2
import numpy


def processImage(image):
    # do stuff
    edges = cv2.Canny(image,100,200)
    numpy.dstack( ( image, edges ) )
    result = image
    return result


FILE_TYPE = ".png"


cwd = os.getcwd()
init_files = glob.glob(cwd + '/**/*' + FILE_TYPE, recursive=True)
files = []
for path in init_files:
    if "result" in path:
        pass
    else:
        files.append(os.path.relpath(path))
print(files)

if not os.path.exists('result'):
    os.mkdir('result')

for image in files:
    cur_image = cv2.imread(image)
    fname = os.path.basename(image)
    # print(fname)
    result_image = processImage(cur_image)
    result_path = cwd + "/result/" + image
    dir_path = result_path[:-len(fname)]
    print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok = True)

    cv2.imwrite(result_path, result_image)
