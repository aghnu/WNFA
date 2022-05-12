from . import image_processing_utilities
import os
import numpy as np

# constance
OUT_RES_WIDTH = 3200
OUT_RES_HEIGHT = 2700
OUT_GRID = 12


'''
idea:
    1. Pick major emotion, and all the other decision are decided by using the combination of major emotion and other emotions number
    2. Art Generation
        - Loop for each layer
            - pick a starting grid position and an ending grid position
                - consider hot map
                - randomly generating the number of grids and shape

            - generating a mask (optional, decided by data and layer type)
                - use random generator, pick 20% ~ 30% grids 
                - everytime, increase the weights of the connecting grids

            - pick a resource, stretch it to the grid size then apply the mask if there is a mask
                - stretching
                    - pick the max(width, height), then stretch it to the grid's width or height
                    - then generating a range from (grid height/width - resource grid height/width)
                    - crop
                    - mask

            - print the result to picture
                - paste the result to picture

'''


'''
Use emotion_data to produce a seed
this seed will be used to generate random number whenever feasible
'''
class ControlledRandomGenerator:
    def __init__(self, emotion_data):
        pass


'''
Generate a grid art when provided with emotion data
'''
class GridArt:
    def __init__(self, emotion_data):
        self.emotion_data = emotion_data
        self.out = np.zeros((OUT_RES_HEIGHT, OUT_RES_WIDTH, 4), dtype=np.ubyte)
    




