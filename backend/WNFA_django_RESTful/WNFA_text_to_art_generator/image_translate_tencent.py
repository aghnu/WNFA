import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client
from tencentcloud.tmt.v20180321 import models as tmt_models
from tencentcloud.ocr.v20181119 import ocr_client
from tencentcloud.ocr.v20181119 import models as ocr_models


def tencent_text_translate(text_cn):

    cred = credential.EnvironmentVariableCredential().get_credential()
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

    req = tmt_models.TextTranslateRequest()
    params = {
        "SourceText": text_cn,
        "Source": "auto",
        "Target": "en",
        "ProjectId": 1262395
    }
    req.from_json_string(json.dumps(params))

    resp = client.TextTranslate(req)

    # response

    resp_dict = json.loads(resp.to_json_string())

    text_en = resp_dict["TargetText"]

    return text_en

def tencent_img_translate(img_base64):

    cred = credential.EnvironmentVariableCredential().get_credential()
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

    req = tmt_models.ImageTranslateRequest()
    params = {
        "SessionUuid": "default",
        "Scene": "doc",
        "Data": img_base64,
        "Source": "zh",
        "Target": "en",
        "ProjectId": 1262395
    }
    req.from_json_string(json.dumps(params))

    resp = client.ImageTranslate(req)

    # process response
    text_cn = []
    text_en = []

    resp_dict = json.loads(resp.to_json_string())
    for val in resp_dict["ImageRecord"]["Value"]:
        text_cn.append(val["SourceText"])
        text_en.append(val["TargetText"])

    return ".".join(text_cn) + ".", ".".join(text_en) + "."

def tencent_handwriting_ocr(img_base64):

    cred = credential.EnvironmentVariableCredential().get_credential()
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

    req = ocr_models.GeneralHandwritingOCRRequest()
    params = {
        "ImageBase64": img_base64
    }
    req.from_json_string(json.dumps(params))

    resp = client.GeneralHandwritingOCR(req)

    # response

    text_cn = []

    resp_dict = json.loads(resp.to_json_string())
    for val in resp_dict["TextDetections"]:
        text_cn.append(val["DetectedText"])

    return "???".join(text_cn) + "???"
