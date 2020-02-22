import requests
import numpy as np
import time
import json
import cv2
import configparser
import base64

if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.read("config.txt")
    url = config.get("faceshifter_client","url")
    Xs_path = config.get("faceshifter_client","source_image_path")
    Xt_path = config.get("faceshifter_client","target_image_path")
    save_path = config.get("faceshifter_client","result_image_save_path")
    with open(Xs_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        X_s = encoded_image.decode('utf-8')
    with open(Xt_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        X_t = encoded_image.decode('utf-8')
    payload = {'source_image': X_s, 'target_image':X_t}
    time1 = time.time()
    r = requests.post(url, data=payload).json()
    time2 = time.time()
    print(time2-time1)
    groundline = {}
    if r['success']:
        result = r['image']
        result = base64.b64decode(result.encode('utf-8'))
        result = cv2.imdecode(np.frombuffer(result, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('image',result)
        cv2.imwrite(save_path,result*255)
        cv2.waitKey(0)


