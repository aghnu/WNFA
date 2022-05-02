import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

def tencent_img_translate(img_base64):
    try:
        cred = credential.ProfileCredential.get_credential()
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

        req = models.ImageTranslateRequest()
        params = {
            "SessionUuid": "default",
            "Scene": "doc",
            "Data": img_base64,
            "Source": "auto",
            "Target": "en",
            "ProjectId": 1262395
        }
        req.from_json_string(json.dumps(params))

        resp = client.ImageTranslate(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
    
    return None
