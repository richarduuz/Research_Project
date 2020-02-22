import sys
sys.path.append('./face_modules/')
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
from face_modules.model import Backbone, Arcface, MobileFaceNet, Am_softmax, l2_norm
from network.AEI_Net import *
from face_modules.mtcnn import *
import cv2
import PIL.Image as Image
import numpy as np
import glob
import configparser
import os
import time

time1 = time.time()

config=configparser.ConfigParser()
config.read("config.txt")
source_image_path  = config.get("video_inference","source_image_path")
target_video_path  = config.get("video_inference","target_video_path")
target_frames_path = config.get("video_inference","target_frames_path")
result_frames_path = config.get("video_inference","result_frames_path")
result_video_save_path  = config.get("video_inference","result_video_save_path")
fps = int(config.get("video_inference","fps"))

print("start transfer video to frames")
# transfer video to frames
cap = cv2.VideoCapture(target_video_path)
sucess = cap.isOpened()
frame_count = 0
if sucess == False:
    print("error opening video stream or file!")
try:
    while sucess:
        sucess, frame = cap.read()
        frame_path = os.path.join(target_frames_path,'%08d.jpg'%frame_count)
        cv2.imwrite(frame_path, frame)
        if (frame_count%50==0):
            print("%dth frame has been processed" %frame_count)
        frame_count += 1
except Exception as e:
    print("video has been prcessed to frames")
cap.release()

print("start load models")
# load models
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

# load source image
Xs_raw = cv2.imread(source_image_path)
Xs = detector.align(Image.fromarray(Xs_raw[:, :, ::-1]), crop_size=(256, 256))
Xs_raw = np.array(Xs)[:, :, ::-1]
Xs = test_transform(Xs)
Xs = Xs.unsqueeze(0).cuda()

# calculate embedding
with torch.no_grad():
    embeds = arcface(F.interpolate(Xs[:, :, 19:237, 19:237], (112, 112), mode='bilinear', align_corners=True))

# load frames
files = glob.glob(os.path.join(target_frames_path,'*.*g'))
files.sort()
ind = 0

# generate mask
mask = np.zeros([256, 256], dtype=np.float)
for i in range(256):
    for j in range(256):
        dist = np.sqrt((i-128)**2 + (j-128)**2)/128
        dist = np.minimum(dist, 1)
        mask[i, j] = 1-dist
mask = cv2.dilate(mask, None, iterations=20)
size = ()
# inference
print("start inference")
for file in files:
    Xt_path = file
    Xt_raw = cv2.imread(Xt_path)
    try:
        Xt, trans_inv = detector.align(Image.fromarray(Xt_raw[:, :, ::-1]), crop_size=(256, 256), return_trans_inv=True)
    except Exception as e:
        print('skip one frame')
        continue

    if Xt is None:
        continue

    Xt_raw = Xt_raw.astype(np.float)/255.0

    size = (Xt_raw.shape[1],Xt_raw.shape[0])

    Xt = test_transform(Xt)

    Xt = Xt.unsqueeze(0).cuda()
    with torch.no_grad():
        Yt, _ = G(Xt, embeds)
        Yt = Yt.squeeze().detach().cpu().numpy().transpose([1, 2, 0])*0.5 + 0.5
        Yt = Yt[:, :, ::-1]
        Yt_trans_inv = cv2.warpAffine(Yt, trans_inv, (np.size(Xt_raw, 1), np.size(Xt_raw, 0)), borderValue=(0, 0, 0))
        mask_ = cv2.warpAffine(mask,trans_inv, (np.size(Xt_raw, 1), np.size(Xt_raw, 0)), borderValue=(0, 0, 0))
        mask_ = np.expand_dims(mask_, 2)
        Yt_trans_inv = mask_*Yt_trans_inv + (1-mask_)*Xt_raw
        save_path = os.path.join(result_frames_path,'%08d.jpg'%ind)
        cv2.imwrite(save_path, Yt_trans_inv*255)
        if(ind % 50 == 0):
            print("%dth frame has been processed"%ind)
        ind += 1

print("start generate video")
videowriter = cv2.VideoWriter(result_video_save_path,cv2.VideoWriter_fourcc('M','J','P','G'),fps,size)

files = glob.glob(os.path.join(result_frames_path,'*.*g'))
files.sort()
count = 0
for file in files:
    img = cv2.imread(file)
    videowriter.write(img)
    if(count % 50 == 0):
        print("%dth frames has been convert to video" %count)
    count +=1

time2 = time.time()
print("total processing time is %f"%(time2-time1))
