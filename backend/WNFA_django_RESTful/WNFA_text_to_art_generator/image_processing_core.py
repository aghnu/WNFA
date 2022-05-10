from copyreg import constructor
from dataclasses import replace
from telnetlib import AO
import numpy as np
import os
from skimage import io, color, img_as_float, feature, transform, exposure
from PIL import Image
from skimage.util import img_as_ubyte
import cv2


# constance
OUT_RES_WIDTH = 3189
OUT_RES_HEIGHT = 2362

# utility functions
def getImgPath(relative_path):
    return relative_path

# NO blur on pixel, use linear calculation for scaling
# futrue features:
#   - preprocessing image for better loading time, and META data on color/shape 
#   - adding more run time META data for better control of the placement/editing

# META data JSON


# TODOs
#   - implementing functions
#       - hot map
#   - META data JSON
#       - what should be included
#   - normalize and organize the emotion data
#       - ranking
#       - normalization


# To Solve
#   - 1. Generating Pipeline
#           - consider hotmap, meta data
#           - before enter the pipeline calculating all resource image META and pick a plan
#   - 2. normalize emotion data, how to put them to use, distincation between two poems, picked a main emotion and start from there
#   - 3. META data setup


class Output:
    def __init__(self):
        self.hotmap = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH), dtype=np.ubyte)     # hotmap used for crowding
        self.output = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH), dtype=np.ubyte)     # output image

# processing functions
def addAlphaChannel(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

def scaleImageToRes(img_numpy, size_height, size_width):
    return img_as_ubyte(transform.resize(img_numpy, (size_height, size_width)))

def pasteImageToImage(image_src, image_res, position_tuple):
    # position tuple
    # (row, col)
    image_src[position_tuple[0]:position_tuple[0]+image_res.shape[0],position_tuple[1]:position_tuple[1]+image_res.shape[1]] = image_res

    return image_src

def maskImageFromMap(image_src, image_map, replace_value):
    # two image, same size, one is a binary image used as map.
    # image map is grey scale
    # all black pixel is kept but white pixel is removed
    for row in range(image_src.shape[0]):
        for col in range(image_src.shape[1]):
            if image_map == 0:
                image_src[row,col] = replace_value
    return image_src

def pasteImageToImageTransparent(image_src, image_res, position_tuple):
    # apply a transparent image to image_src

    img_blend = image_src[position_tuple[0]:position_tuple[0]+image_res.shape[0],position_tuple[1]:position_tuple[1]+image_res.shape[1]]

    image_overlay = Image.fromarray(image_res)
    image_blend_result = Image.fromarray(img_blend)
    image_blend_result.paste(image_overlay, mask=image_overlay)
    
    image_src[position_tuple[0]:position_tuple[0]+image_res.shape[0],position_tuple[1]:position_tuple[1]+image_res.shape[1]] = np.array(image_blend_result)
    return image_src

def rotateImage(image_src, angle):
    # angle: float - Rotation angle in degrees in counter-clockwise direction.
    return img_as_ubyte(transform.rotate(image_src, angle))


def applyAlphaValue(image_src, alpha_value):
    image_src[:,:,3] = alpha_value
    return image_src

def applyFunctionToImage(image_src, function):
    image_src[:,:] = function(image_src[:,:])

def clusterFilter(img_src, size_block, size_between):
    pass

def textToImage(text, font, size):
    # given text, font, position and a size return an image of this text with give size
    pass

def edgeDetection(image_src):
    # take in an image, return a binary image with edges
    pass


def generatingSingleColorImg(value):
    # return a 4*4 image array with the given rgba value
    return np.array([
        [value,value],
        [value,value],
    ], dtype=np.ubyte)

def cropImage(image_src, size_tuple, position_tuple):
    return image_src[position_tuple[0]:position_tuple[0]+size_tuple[0],position_tuple[1]:position_tuple[1]+size_tuple[1]]

img1 = addAlphaChannel(io.imread(getImgPath('art_assets/Background/anger-bg1.jpg')))
img2 = addAlphaChannel(io.imread(getImgPath('art_assets/Background/anger-bg2.jpg')))
img2 = scaleImageToRes(img2, img1.shape[0], img1.shape[1])
img2 = cropImage(img2, (500,500),(0,0))
img2 = scaleImageToRes(img2, 300, 300)
img2 = applyAlphaValue(img2, 150)
img2 = rotateImage(img2, 60)


out = pasteImageToImageTransparent(img1, img2, (0,0))

# io.imsave("Test.png", img2)
io.imsave("Test.png", out)