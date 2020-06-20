#!/usr/bin/env python3
# COPY THIS SCRIPT TO THE LOCATION OF "IMAGES" FOLDER CONTAINING ALL IMAGES
# Note: same location as labelme_manipulation script

import glob
import os
import cv2
import numpy
from shutil import copy2
from natsort import natsorted # deals with python sorting weirdness (images with varying # of digits at end)

FILE_TYPE = ".png"
IMAGE_DIR = "/home/tanner/Cinderblock/images"
# cwd = IMAGE_DIR
cwd = os.getcwd()

# TODO:
# enable command line input to specify processing technique

def saveResult(result_image, image_path):
    fname = os.path.basename(image_path)
    # print(fname)
    result_path = cwd + "/processed_images/" + image_path
    dir_path = result_path[:-len(fname)]
    # print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok = True)
    # print("RESULT PATH: " + result_path)
    # print("RESULT SHAPE: " + str(result_image.shape))
    cv2.imwrite(result_path, result_image)

    # hacked-together method of getting .json files copied over
    try:
        json_path = image_path[:-len(FILE_TYPE)]
        json_path = json_path + ".json"
        save_json_path = result_path[:-len(FILE_TYPE)]
        save_json_path = save_json_path + ".json"
        # print("COPYING " + json_path + " TO " + save_json_path)
        copy2(json_path, save_json_path)
    except:
        print("no .json file associated with current image")

def processDir_TempDisparity(fnames):
    # need to process one directory at a time, skip first image
        # requires passing current directory list of images
    # idea is that each image will have a 4th channel of the differences between it and the previous image
    # therefore first image in directory will have nothing in the 4th channel
    # from skimage.measure import compare_ssim
    from skimage.metrics import structural_similarity as compare_ssim
    import imutils
    firstImage = True
    for i in range(len(fnames)):
        if firstImage:
            firstImage = False
            pass
        else:
            # load images in grayscale
            img1 = cv2.imread(fnames[i], 0)
            img2 = cv2.imread(fnames[i-1], 0) # comparing to previous image
            # compute difference via SSIM, make image we can add to 4th channel
            (score, diff) = compare_ssim(img1, img2, full=True)
            diff = (diff * 255).astype("uint8")
            # cv2.imshow("diff", diff)
            # cv2.waitKey(10)
            original_img1 = cv2.imread(fnames[i], -1)
            result_image = numpy.dstack((original_img1, diff))
            image_path = fnames[i]
            saveResult(result_image, image_path)

def processDir_StereoDisparity(fnames):
    # needs to have matching frames from left and right directories for each subset

    # load left and right matching frames in grayscale
    # make left-based disparity image
    # flip images (?)
        # mirror each one? or switch which one we call left vs right?
    # make right-based disparity image
    # save 4th channel in each

    # TODO: update saveResult to use os.path.dirname function instead of string manipulation
    subset_path = os.path.dirname(os.path.dirname(fnames[0]))
    left_fnames = natsorted(glob.glob(subset_path + '/left/*' + FILE_TYPE))
    right_fnames = natsorted(glob.glob(subset_path + '/right/*' + FILE_TYPE))
    # print("LEFT: " + str(left_fnames))
    # print("RIGHT: " + str(right_fnames))
    for i in range(len(left_fnames)):
        # make sure there is a matching frame in right_fnames
            # last 3 characters of each frame (not including file extension) must match
                # still works for 2-digit numbered images
        test_left = left_fnames[i][-(3 + len(FILE_TYPE)):]
        # print("TEST: " + test_left)
        test_right = right_fnames[i][-(3 + len(FILE_TYPE)):]
        if test_left == test_right:
            # frames match
            # compute left-based disparity
            left_img = cv2.imread(left_fnames[i], 0)
            right_img = cv2.imread(right_fnames[i], 0)
            stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
            left_disparity = stereo.compute(left_img, right_img).astype("uint8")

            # compute right-based disparity
            left_flipped = cv2.flip(left_img, 1)
            right_flipped = cv2.flip(right_img, 1)
            right_disparity = stereo.compute(right_flipped, left_flipped).astype("uint8")

            cv2.imshow("left-based", left_disparity)
            cv2.imshow("right-based", right_disparity)
            cv2.waitKey(10)

        else:
            pass


def processDir_Batch(fnames):
    # convert the current + next 4 images to grayscale
    # concatenate all 5 and save into the 4th channel of image1
    # ex: image1 will have in its 4th channel data from img1, img2, img3, img4, img5
        # image2 will have in its 4th channel data from img2, img3, img4, img5, img6 and so on
    # skips images that don't have 4 subsequent images in the directory
    for i in range(len(fnames)):
        try:
            print("new batch")
            # load next 5 images and convert to grayscale
            image_path = fnames[i]
            img5 = cv2.imread(fnames[i+4], 0)
            img4 = cv2.imread(fnames[i+3], 0)
            img3 = cv2.imread(fnames[i+2], 0)
            img2 = cv2.imread(fnames[i+1], 0)
            img1 = cv2.imread(fnames[i], 0)

            original_img1 = cv2.imread(fnames[i], 1)
            img_sum = img1 + img2 + img3 + img4 + img5
            result_image = numpy.dstack((original_img1, img_sum))
            print("IMAGE PATH (passed to save result): " + image_path)
            print("saving result!")
            saveResult(result_image, image_path)

        # except error as e:
        #     print(e)

        except:
            print("less than 5 images left in directory")
            # print("current image: " + fnames[i])
            # unchanged_image = cv2.imread(fnames[i], 1)
            # unchanged_path = fnames[i]
            # saveResult(unchanged_image, unchanged_path)
            # print("saved unchanged image!")
            # note: this will result in runnning darknet on images with different formatting
            #       some will have 4th channel, others not. may cause issues / errors?
            #       could possibly fix by giving these images 4th channel of all zeros?



def processDir_Canny(fnames):
    for fname in fnames:
        image = cv2.imread(fname, -1)
        edges = cv2.Canny(image,100,200)
        edges = edges.astype('uint8')
        result_image = numpy.dstack((image, edges))
        saveResult(result_image, fname)


def processDir_MOG(fnames):
    for fname in fnames:
        backSub = cv2.createBackgroundSubtractorMOG2()
        image = cv2.imread(fname)
        fgMask = backSub.apply(image)
        print("FGMASK SHAPE: " + str(fgMask.shape))
        cv2.imshow('Frame', image)
        cv2.imshow('FG Mask', fgMask)
        fgMask = fgMask.astype('uint8')
        cv2.waitKey(10)
        result_image = numpy.dstack((image, fgMask))
        saveResult(result_image, fname)

def getAllFilePathList():
    init_files = glob.glob(cwd + '/**/*' + FILE_TYPE, recursive=True)
    files = []
    for path in init_files:
        if "processed_images" in path:
            pass
        else:
            files.append(os.path.relpath(path))
    print(files)
    return files

def getDirectoryList():
    directories = None
    return directories

if __name__ == "__main__":
    #files = getAllFilePathList()

    base_dirs = sorted(glob.glob("images/*"))
    for base_dir in base_dirs:
        print("DIR: " + base_dir)

        sub_dirs = sorted(glob.glob(base_dir + "/*"))
        for sub_dir in sub_dirs:
            print("SUB DIR: " + sub_dir)
            fnames = natsorted(glob.glob(sub_dir + "/*" + FILE_TYPE, recursive=True))
            # process current directory and save results
            # processDir_Batch(fnames)
            processDir_StereoDisparity(fnames)

    # if not os.path.exists('processed_images'):
    #     os.mkdir('processed_images')
    #
    # for image in files:
    #     cur_image = cv2.imread(image)
    #     fname = os.path.basename(image)
    #     # print(fname)
    #     result_image = processImage_MOG(cur_image)
    #     # save resulting image
    #     result_path = cwd + "/processed_images/" + image
    #     dir_path = result_path[:-len(fname)]
    #     print(dir_path)
    #     print
    #     if not os.path.exists(dir_path):
    #         os.makedirs(dir_path, exist_ok = True)
    #
    #     cv2.imwrite(result_path, result_image)
