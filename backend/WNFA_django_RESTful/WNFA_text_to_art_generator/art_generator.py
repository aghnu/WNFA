from WNFA_text_to_art_generator.image_translate_tencent import tencent_img_translate
from WNFA_text_to_art_generator.image_processing import GridArt, is_chinese_char
from WNFA_text_to_art_generator.emotion_analysis import predict_emo

import base64
import io
from PIL import Image
import numpy as np


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

    def __init__(self, img_base64):
        img_decoded = base64.b64decode(img_base64)
        img_pil = Image.open(io.BytesIO(img_decoded))
        self.img_np = np.array(img_pil)
        self.img_base64 = str(img_base64)

    def generate(self):

        cn_text, eng_text = tencent_img_translate(self.img_base64)
        # cn_text, eng_text = ("测试文本", "testing text")

        if len([c for c in list(cn_text) if is_chinese_char(c)]) == 0:
            raise ValueError

        emotion_data = predict_emo(eng_text)
        record = {
            'base64': self.img_base64,
            'text_cn': cn_text,
            'text_en': eng_text
        }
        art = GridArt(emotion_data, record)
        out = art.gen()
        
        img_pil = Image.fromarray(out)        
        buff = io.BytesIO()
        img_pil.save(buff, format="JPEG")

        return ArtOBJ(buff.getvalue(), eng_text, cn_text)