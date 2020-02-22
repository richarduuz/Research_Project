# Model C - FaceShifer

This is the reproducing version of FaceShiter

Paper Reference: https://arxiv.org/pdf/1912.13457.pdf

Code Reference: https://github.com/taotaonice/FaceShifter

## Requirements
* Python 3.7
* torch 1.4.0
* torchvison 0.5.0
* opencv-python 4.2.0
* numpy 1.18.1
* Flask
* flask_cors
* requests

You can install these packages by pip
```
pip install -r requirements.txt
```
If you want to train the model, you have to install apex, you can download and install from the Nvidia/apex: https://github.com/NVIDIA/apex

## How to use FaceShifter
### Download Pre-trained Weights
* URL for download pre-trained weights of arcface: https://drive.google.com/open?id=15nZSJ2bAT3m-iCBqP3N_9gld5_EGv4kp, then put it to the directory "face_modules/"
* URL for download pre-trained weights of AEI-Net: https://drive.google.com/open?id=1iANX7oJoXCEECNzBEW1xOpac2tDOKeu9, then put it to the directory "saved_models/"
### image_inference
You can swap face of two images. One is source image and another is target image
* open config.txt
* set parameters of "source_image_path", "target_image_path", and "result_image_save_path" in section [image_inference]
* run `python image_inference.py`
### video_inference
You can swap the faces in video by one source image and one target video
* open config.txt
* set parameters of "source_image_path", "target_video_path", "target_frames_path", "result_frames_path", "result_video_save_path", and "fps" in section [video_inference]
* run `python video_inference.py`
### train
You can train the model
* open config.txt
* set parameters of "dataset_path" in section [train]
* run `python train.py`
* You can modify parameters of BatchSize, epoch,learning rate in train.py
### faceshifter_server
You can deploy model server.
* open config.txt
* set parameters of "port" in section [faceshifter_server]
* run `python faceshifter_server.py`
### faceshifter_client
When you deploy the server, you can test it by python-version client
* open config.txt
* set parameters of "url", "source_image_path", "target_image_path", "result_image_save_path" in section [faceshifter_client]
* run `python faceshifter_client.py`
