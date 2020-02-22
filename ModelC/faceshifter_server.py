import time
import numpy as np
import flask
import sys
import torch
sys.path.append('./face_modules/')
import torchvision.transforms as transforms
import torch.nn.functional as F
from face_modules.model import Backbone, Arcface, MobileFaceNet, Am_softmax, l2_norm
from network.AEI_Net import *
from face_modules.mtcnn import *
import cv2
import PIL.Image as Image
import numpy as np
from flask_cors import CORS
import base64
import configparser

app = flask.Flask(__name__)
CORS(app)

@app.route('/faceshifter', methods=['POST'])
def serve():
    data = {"success":False}
    detector = MTCNN()
    device = torch.device('cuda')
    G = AEI_Net(c_id=512)
    G.eval()
    G.load_state_dict(torch.load('./saved_models/G_latest.pth', map_location=torch.device('cpu')))
    G = G.cuda()
    arcface = Backbone(50, 0.6, 'ir_se').to(device)
    arcface.eval()
    arcface.load_state_dict(torch.load('./face_modules/model_ir_se50.pth', map_location=device), strict=False)

    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    if flask.request.method == 'POST':
        st = time.time()
        metadata = flask.request.form
        source_image = metadata['source_image']
        target_image = metadata['target_image']
        source_image = base64.b64decode(source_image.encode('utf-8'))
        Xs_raw = cv2.imdecode(np.frombuffer(source_image, np.uint8), cv2.IMREAD_COLOR)
        target_image = base64.b64decode(target_image.encode('utf-8'))
        Xt_raw = cv2.imdecode(np.frombuffer(target_image, np.uint8), cv2.IMREAD_COLOR)
        Xs = detector.align(Image.fromarray(Xs_raw[:, :, ::-1]), crop_size=(256, 256))
        Xs_raw = np.array(Xs)[:, :, ::-1]
        Xs = test_transform(Xs)
        Xs = Xs.unsqueeze(0).cuda()
        with torch.no_grad():
            embeds = arcface(F.interpolate(Xs[:, :, 19:237, 19:237], (112, 112), mode='bilinear', align_corners=True))
        Xt, trans_inv = detector.align(Image.fromarray(Xt_raw[:, :, ::-1]), crop_size=(256, 256), return_trans_inv=True)
        Xt_raw = Xt_raw.astype(np.float)/255.0
        Xt = test_transform(Xt)
        Xt = Xt.unsqueeze(0).cuda()
        mask = np.zeros([256, 256], dtype=np.float)
        for i in range(256):
            for j in range(256):
                dist = np.sqrt((i-128)**2 + (j-128)**2)/128
                dist = np.minimum(dist, 1)
                mask[i, j] = 1-dist
        mask = cv2.dilate(mask, None, iterations=20)

        with torch.no_grad():
            Yt, _ = G(Xt, embeds)
            Yt = Yt.squeeze().detach().cpu().numpy().transpose([1, 2, 0])*0.5 + 0.5
            Yt = Yt[:, :, ::-1]
            Yt_trans_inv = cv2.warpAffine(Yt, trans_inv, (np.size(Xt_raw, 1), np.size(Xt_raw, 0)), borderValue=(0, 0, 0))
            mask_ = cv2.warpAffine(mask,trans_inv, (np.size(Xt_raw, 1), np.size(Xt_raw, 0)), borderValue=(0, 0, 0))
            mask_ = np.expand_dims(mask_, 2)
            Yt_trans_inv = mask_*Yt_trans_inv + (1-mask_)*Xt_raw
        img_data = Yt_trans_inv*255
        retval, buffer = cv2.imencode('.jpg', img_data)
        pic_str = base64.b64encode(buffer)
        pic_str = pic_str.decode()
        data['success'] = True
        data['image'] = pic_str
        st = time.time() - st
        print(f'process time: {st} sec')
        return flask.jsonify(data)

if __name__ == '__main__':
    print("Please wait until server has fully started")
    config=configparser.ConfigParser()
    config.read("config.txt")
    port = config.get("faceshifter_server","port")
    app.run(host='0.0.0.0', port=port, debug=False)
