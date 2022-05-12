import numpy as np
import os
from skimage import io, color, img_as_float, feature, transform, exposure
from PIL import Image, ImageDraw, ImageFont
from skimage.util import img_as_ubyte
import cv2
import json
import math
import textwrap
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

# constance
OUT_RES_WIDTH = 3200
OUT_RES_HEIGHT = 2700
OUT_GRID = 12

# utility functions
def getPath(relative_path):
    return relative_path

# class Output:
#     def __init__(self):
#         self.hotmap = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH), dtype=np.ubyte)     # hotmap used for crowding
#         self.output = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH), dtype=np.ubyte)     # output image

# processing functions
def addAlphaChannel(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

def convertToGreyScale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def scaleImageToRes(img_src, size_height, size_width):
    img_pil = Image.fromarray(img_src).resize([size_width, size_height], resample=Image.Resampling.NEAREST)
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

def generatingSingleColorImg(value):
    # return a 4*4 image array with the given rgba value
    return np.array([
        [value,value],
        [value,value],
    ], dtype=np.ubyte)

def charToImage(char, font_path, size, color):
    # given text, font, position and a size return an image of this text with give size
    img = generatingSingleColorImg((255,255,255,0))
    img_resized = scaleImageToRes(img, size, size)
    img_pil = Image.fromarray(img_resized)

    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, size)

    draw.text((0,0), char, fill=color, font=font)

    return np.array(img_pil)

def textToImage(text, font_path, height_width, size, color):
    img = generatingSingleColorImg((255,255,255,0))
    img_resized = scaleImageToRes(img, height_width[0], height_width[1])
    img_pil = Image.fromarray(img_resized)

    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, size)

    text_str = "\n".join(textwrap.wrap(text, width=height_width[1]*2//size))
    draw.text((0,0), text_str, fill=color, font=font)

    return np.array(img_pil)


def edgeDetection(image_src):
    # take in an image, return a binary image with edges
    pass


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

def loadImageFromIO(path):
    return img_as_ubyte(addAlphaChannel(io.imread(path)))

def maskToImage(img, mask_layer_value, res, startingPos, gridSize):
    # mask is the same size

    hs = startingPos[0]
    he = startingPos[0] + gridSize[0]

    ws = startingPos[1]
    we = startingPos[1] + gridSize[1]

    mask,layer,value = mask_layer_value
    res_resized = scaleImageToRes(res, gridSize[0], gridSize[1])

    img[hs:he,ws:we][mask[hs:he,ws:we][:,:,layer] == value] = res_resized[mask[hs:he,ws:we][:,:,layer] == value]

    return img
    
# def maskTextToImageInvert(img, mask_layer_value, res, startingPos, gridSize):
#     # mask is the same size

#     hs = startingPos[0]
#     he = startingPos[0] + gridSize[0]

#     ws = startingPos[1]
#     we = startingPos[1] + gridSize[1]

#     mask,layer,value = mask_layer_value
#     res_resized = scaleImageToRes(res, gridSize[0], gridSize[1])
#     print(res_resized.shape)
#     # img[hs:he,ws:we][mask[hs:he,ws:we][:,:,layer] == value] = res_resized[mask[hs:he,ws:we][:,:,layer] == value]
#     img[hs:he,ws:we][res_resized[:,:,3]>0][mask[hs:he,ws:we][res_resized[:,:,3]>0][:,:,layer] == value] = [255,255,255,255]

#     return img

def gridToSize(gridHeight, gridWidth):
    return (gridHeight * (OUT_RES_HEIGHT//OUT_GRID), gridWidth * (OUT_RES_WIDTH//OUT_GRID))

def gridToPos(gridStartHeight, gridStartWidth):
    return (gridStartHeight * (OUT_RES_HEIGHT//OUT_GRID), gridStartWidth * (OUT_RES_WIDTH//OUT_GRID))



# class GridArt: 
#     def __init__(self):
#         self.output = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH, 4), dtype=np.ubyte)     # output image
#         with open("art_assets/Grids/META.json") as j:
#             self.grid_meta = json.load(j)    
        
#     def generate(self, emotion_data):
#         emotion = "anger"
#         grid = io.imread("art_assets/Grids/{emotion}/grid.png".format(emotion = emotion))
#         layers = list(self.grid_meta[emotion].keys())

#         for layer in layers:
#             works = list(self.grid_meta[emotion][layer].keys())
#             for work in works:
#                 img_path_list = self.grid_meta[emotion][layer][work][0].split('-')           # 0 is the selected option, if there are multiple options
#                 img_path = 'assets/'
#                 for path in img_path_list:
#                     img_path += path + '/'

#                 imgs = filter(lambda str: str.split('.')[1] == 'png' or str.split('.')[1] == 'jpg', os.listdir(img_path))
#                 img_selected = imgs[0]                                                      # 0 is the selected option
#                 io.imread(img_path + img_selected)


#     def apply_rules(self, img):

# (height, width)


fake_code = '''
#     def generate(self, emotion_data):
#         emotion = "anger"
#         grid = io.imread("art_assets/Grids/{emotion}/grid.png".format(emotion = emotion))
#         layers = list(self.grid_meta[emotion].keys())

#         for layer in layers:
#             works = list(self.grid_meta[emotion][layer].keys())
#             for work in works:
#                 img_path_list = self.grid_meta[emotion][layer][work][0].split('-')           # 0 is the selected option, if there are multiple options
#                 img_path = 'assets/'
#                 for path in img_path_list:
#                     img_path += path + '/'

#                 imgs = filter(lambda str: str.split('.')[1] == 'png' or str.split('.')[1] == 'jpg', os.listdir(img_path))
#                 img_selected = imgs[0]                                                      # 0 is the selected option
#                 io.imread(img_path + img_selected)
'''

fake_binary_number = '''
0111000011001010101010000000000001010101011100000000000000001101011010101
0101010101000001100101010111111110101010000000001010101000001010101010101
0000000000000000110101101010110101111111101010100000000001100101010101000
0000000001010110101011010111111110101010000101101010110101111111101010100
0111000011001010101010000000000001010101011100000000000000001101011010101
0101010101000001100101010111111110101010000000001010101000001010101010101
0000000000000000110101101010110101111111101010100000000001100101010101000
0000000001010110101011010111111110101010000101101010110101111111101010100
'''

def demo_anger_1():

    out = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH, 4), dtype=np.ubyte)
    out[:,:] = [255,255,255,255]
    grid = io.imread('art_assets/Grids/anger/grid.png')
    grid = scaleImageToRes(grid, OUT_RES_HEIGHT, OUT_RES_WIDTH)

    # a: 
    bg = loadImageFromIO('art_assets/1/1/anger/anger-bg1.jpg')
    bg = scaleImageToRes(bg, OUT_RES_HEIGHT, OUT_RES_WIDTH)

    out[grid[:,:,0] == 255] = bg[grid[:,:,0] == 255]

    # b:
    # 2-2
    res_startPos = (0,0)
    res_size = (2, 8)

    res = loadImageFromIO('art_assets/2/2/17.png')
    res = cropImage(res, (math.floor(res.shape[1]/res_size[1] * res_size[0]), res.shape[1]), (res.shape[0]//2, 0))

    out = maskToImage(out, (grid, 1, 200), res, gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))
    # 2-3
    res_startPos = (2,8)
    res_size = (4, 4)

    res = loadImageFromIO('art_assets/2/3/风雨.png')
    out = maskToImage(out, (grid, 1, 150), res, gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))

    # 2-4
    res_startPos = (6,10)
    res_size = (2, 2)

    res = loadImageFromIO('art_assets/2/4/01.png')
    out = maskToImage(out, (grid, 1, 100), res, gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))

    # text
    # 4-3
    res_startPos = (0,0)
    res_size = (4, 4)

    res = charToImage("落", 'art_assets/4/3/HYBaoSongJ.ttf', gridToSize(*res_size)[1], "#505050")
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out_selected = out.copy()
    out_selected = cropImage(out_selected, gridToSize(*res_size), gridToPos(*res_startPos))

    out_selected = maskTextToImageInvert(out_selected, res)

    # out = maskTextToImageInvert(out, (grid, 2, 255), np.invert(res), gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))
    out = pasteImageToImageTransparent(out, out_selected, gridToPos(*res_startPos))

    # 4-2
    res_startPos = (4,0)
    res_size = (4, 8)

    res = textToImage(fake_code, 'art_assets/4/2/RadioNewsman.ttf', gridToSize(*res_size), 100, "#505050")
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out_selected = out.copy()
    out_selected = cropImage(out_selected, gridToSize(*res_size), gridToPos(*res_startPos))

    out_selected = maskTextToImageInvert(out_selected, res)
    out = pasteImageToImageTransparent(out, out_selected, gridToPos(*res_startPos))

    # 4-1
    res_startPos = (8,10)
    res_size = (4, 2)

    res = textToImage(fake_binary_number, 'art_assets/4/2/RadioNewsman.ttf', gridToSize(*res_size), 50, "#505050")
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out_selected = out.copy()
    out_selected = cropImage(out_selected, gridToSize(*res_size), gridToPos(*res_startPos))

    out_selected = maskTextToImageInvert(out_selected, res)
    out = pasteImageToImageTransparent(out, out_selected, gridToPos(*res_startPos))

    # decoration
    # 5
    res_startPos = (0,4)
    res_size = (8, 8)

    res = loadImageFromIO('art_assets/5/1/01.png')
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out = pasteImageToImageTransparent(out, res, gridToPos(*res_startPos))

    out = removeAlpha(out)
    io.imsave("test.png", out)

def demo_anger_2():

    out = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH, 4), dtype=np.ubyte)
    out[:,:] = [255,255,255,255]
    grid = io.imread('art_assets/Grids/anger/grid.png')
    grid = scaleImageToRes(grid, OUT_RES_HEIGHT, OUT_RES_WIDTH)

    # a: 
    bg = loadImageFromIO('art_assets/1/1/anger/anger-bg1.jpg')
    bg = scaleImageToRes(bg, OUT_RES_HEIGHT, OUT_RES_WIDTH)

    out[grid[:,:,0] == 255] = bg[grid[:,:,0] == 255]

    # b:
    # 2-2
    res_startPos = (0,0)
    res_size = (2, 8)

    res = loadImageFromIO('art_assets/2/2/17.png')
    res = cropImage(res, (math.floor(res.shape[1]/res_size[1] * res_size[0]), res.shape[1]), (res.shape[0]//2, 0))

    out = maskToImage(out, (grid, 1, 200), res, gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))
    # 2-3
    res_startPos = (2,8)
    res_size = (4, 4)

    res = loadImageFromIO('art_assets/2/3/风雨.png')
    out = maskToImage(out, (grid, 1, 150), res, gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))

    # 2-4
    res_startPos = (6,10)
    res_size = (2, 2)

    res = loadImageFromIO('art_assets/2/4/01.png')
    out = maskToImage(out, (grid, 1, 100), res, gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))

    # text
    # 4-3
    res_startPos = (0,0)
    res_size = (4, 4)

    res = charToImage("落", 'art_assets/4/3/HYBaoSongJ.ttf', gridToSize(*res_size)[1], "#505050")
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out_selected = out.copy()
    out_selected = cropImage(out_selected, gridToSize(*res_size), gridToPos(*res_startPos))

    out_selected = maskTextToImageInvert(out_selected, res)

    # out = maskTextToImageInvert(out, (grid, 2, 255), np.invert(res), gridToPos(res_startPos[0], res_startPos[1]), gridToSize(res_size[0], res_size[1]))
    out = pasteImageToImageTransparent(out, out_selected, gridToPos(*res_startPos))

    # 4-2
    res_startPos = (4,0)
    res_size = (4, 8)

    res = textToImage(fake_code, 'art_assets/4/2/RadioNewsman.ttf', gridToSize(*res_size), 100, "#505050")
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out_selected = out.copy()
    out_selected = cropImage(out_selected, gridToSize(*res_size), gridToPos(*res_startPos))

    out_selected = maskTextToImageInvert(out_selected, res)
    out = pasteImageToImageTransparent(out, out_selected, gridToPos(*res_startPos))

    # 4-1
    res_startPos = (8,10)
    res_size = (4, 2)

    res = textToImage(fake_binary_number, 'art_assets/4/2/RadioNewsman.ttf', gridToSize(*res_size), 50, "#505050")
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out_selected = out.copy()
    out_selected = cropImage(out_selected, gridToSize(*res_size), gridToPos(*res_startPos))

    out_selected = maskTextToImageInvert(out_selected, res)
    out = pasteImageToImageTransparent(out, out_selected, gridToPos(*res_startPos))

    # decoration
    # 5
    res_startPos = (0,4)
    res_size = (8, 8)

    res = loadImageFromIO('art_assets/5/1/01.png')
    res = scaleImageToRes(res, *gridToSize(*res_size))

    out = pasteImageToImageTransparent(out, res, gridToPos(*res_startPos))

    out = removeAlpha(out)
    io.imsave("test.png", out)


demo_anger_1()

















# # img1 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg1.jpg')))
# # img2 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg2.jpg')))
# # img2 = scaleImageToRes(img2, img1.shape[0], img1.shape[1])
# # img2 = cropImage(img2, (500,500),(0,0))
# # img2 = scaleImageToRes(img2, 300, 300)
# # img2 = applyAlphaValue(img2, 150)
# # img2 = rotateImage(img2, 60)

# img1 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg6.jpg')))
# # img1 = generatingSingleColorImg((0,0,0,255))
# img1 = scaleImageToRes(img1, 1000,1000)

# img2 = addAlphaChannel(io.imread(getPath('art_assets/Background/anger-bg6.jpg')))
# # # img2 = generatingSingleColorImg((255,255,255,255))
# img2 = scaleImageToRes(img2, 1000,1000)

# # img1 = pasteImageToImage(img1, img2, (0,500))

# img3 = charToImage("怒", getPath('art_assets/Text/chineseFonts/HYBaoSongF.ttf'), 50, "#555555")
# img3 = scaleImageToRes(img3, 1000,1000)

# # img1 = maskImageFromMap(img1, img3)
# # img1 = pasteImageToImageTransparent(img2, img1, (0,0))

# # img3 = removeSemiAlpha(img3)

# img1 = maskTextToImageInvert(img1, img3)

# # io.imsave("Test.png", img2)
# io.imsave("Test.png", img1)