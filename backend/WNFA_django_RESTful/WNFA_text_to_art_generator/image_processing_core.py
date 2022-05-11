from copyreg import constructor
from dataclasses import replace
from telnetlib import AO
import numpy as np
import os
from skimage import io, color, img_as_float, feature, transform, exposure
from PIL import Image, ImageDraw, ImageFont
from skimage.util import img_as_ubyte
import cv2


# constance
OUT_RES_WIDTH = 3189
OUT_RES_HEIGHT = 2362

# utility functions
def getPath(relative_path):
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

def convertToGreyScale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def scaleImageToRes(img_src, size_height, size_width):
    img_pil = Image.fromarray(img_src).resize([size_height, size_width], resample=Image.Resampling.NEAREST)
    return np.array(img_pil)


def pasteImageToImage(image_src, image_res, position_tuple):
    # position tuple
    # (row, col)
    image_src[position_tuple[0]:position_tuple[0]+image_res.shape[0],position_tuple[1]:position_tuple[1]+image_res.shape[1]] = image_res

    return image_src

def maskImageFromMap(image_src, image_map):
    # two image, same size, one is a binary image used as map.
    # image map is grey scale
    # all none transparent is removed

    image_src[image_map[:,:,3] == 0] = [0,0,0,0]

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
    image_src[:,:,3][image_src[:,:,3] > 0] = alpha_value
    # image_src[:,:,3] = alpha_value
    return image_src

def applyFunctionToImage(image_src, function):
    image_src[:,:] = function(image_src[:,:])

def clusterFilter(img_src, size_block, size_between):
    pass

def charToImage(char, font_path, size, color):
    # given text, font, position and a size return an image of this text with give size
    img = generatingSingleColorImg((0,0,0,0))
    img_resized = scaleImageToRes(img, size, size)
    img_pil = Image.fromarray(img_resized)

    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, size)

    draw.text((0,0), char, fill=color, font=font)

    return np.array(img_pil)


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

def removeAlpha(image_src):
    image_src[:,:,3] = 255
    return image_src

def removeSemiAlpha(image_src):
    image_src[:,:,3][image_src[:,:,3] > 0] = 255
    return image_src

def maskTextToImageInvert(image_src, text):
    # same size
    text = applyAlphaValue(text, 50)
    # image_src[text[:,:,3] > 0] = pixelBinaryValueInvert(image_src[text[:,:,3] > 0])
    image_src[:,:,:3][text[:,:,3] > 0] = np.invert(image_src[:,:,:3][text[:,:,3] > 0])
    return image_src

def pixelBinaryValueInvert(img_vec):
    for i in range(img_vec.shape[0]):
        pixel = img_vec[i]
        pixel_grey = pixel[0] / 3 + pixel[1] / 3 + pixel[2] / 3
        if pixel_grey > 128:
            img_vec[i] = [0,0,0,255]
        else:
            img_vec[i] = [255,255,255,255]

    return img_vec

# img1 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg1.jpg')))
# img2 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg2.jpg')))
# img2 = scaleImageToRes(img2, img1.shape[0], img1.shape[1])
# img2 = cropImage(img2, (500,500),(0,0))
# img2 = scaleImageToRes(img2, 300, 300)
# img2 = applyAlphaValue(img2, 150)
# img2 = rotateImage(img2, 60)

img1 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg6.jpg')))
# img1 = generatingSingleColorImg((0,0,0,255))
img1 = scaleImageToRes(img1, 1000,1000)

img2 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg6.jpg')))
# # img2 = generatingSingleColorImg((255,255,255,255))
img2 = scaleImageToRes(img2, 1000,1000)

# img1 = pasteImageToImage(img1, img2, (0,500))

img3 = charToImage("怒", getPath('art_assets/Text/chineseFonts/HYBaoSongF.ttf'), 50, "#555555")
img3 = scaleImageToRes(img3, 1000,1000)

# img1 = maskImageFromMap(img1, img3)
# img1 = pasteImageToImageTransparent(img2, img1, (0,0))

# img3 = removeSemiAlpha(img3)

img1 = maskTextToImageInvert(img1, img3)

# io.imsave("Test.png", img2)
io.imsave("Test.png", img1)