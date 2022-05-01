from . import emotion_analysis
from . import image_translate_tencent

import base64
import io
from PIL import Image


class ArtOBJ:
    def __init__(self, image_bytes, text_en = None, text_cn = None):
        self.image_bytes = image_bytes
        self.text_en = text_en
        self.text_cn = text_cn

''' 
    this class is used to generate an art in the absence of concrete data, 
    used as a fallback method when data collection fails
'''
class ArtGeneratorRandom:
    def __init__(self):
        pass

'''
    this class is used to generate an art from text data
    text data must be in english
'''
class ArtGeneratorFromText:
    def __init__(self, text_en):
        pass


'''
    this class is used to generate an art from a photo of handwriting chinese character
    photo must be an numpy array
'''
class ArtGeneratorFromImage:

    def __init__(self, img_np):
        self.img_np = img_np

    def generate(self):
        # mockup data

        img_pil = Image.fromarray(self.img_np)        
        buff = io.BytesIO()
        img_pil.save(buff, format="JPEG")

        return ArtOBJ(buff.getvalue(), "Testing_en", "Testing_cn")