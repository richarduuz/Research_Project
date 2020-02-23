# Welcome to our Github repo for COMP90055 Research Project on DeepFake


## Project Objective
Our project aims to find a suitable DeepFake model, in terms of visual quality, inferencing speed and easiness of deploying, to deploy on as Android demo application server. We have uploaded and referenced code of all 3 potential models we selected in addition with our Android application package and server.

## Code Reference
In this repo, there are 3 models we referenced from 3 authors.

**Model A**: [FaceSwap](https://github.com/wuhuikai/FaceSwap).

**Model B**: [Few-shot face translation](https://github.com/shaoanlu/fewshot-face-translation-GAN).

**Model C**: [FaceShifter](https://github.com/taotaonice/FaceShifter)

## Image Results by Each Model

<img src="https://github.com/richarduuz/Research_Project/blob/master/model_a_image_result.jpg" width="400">

<img src="https://github.com/richarduuz/Research_Project/blob/master/model_b_image_result.jpg" width="400">

<img src="https://github.com/richarduuz/Research_Project/blob/master/model_c_image_result.jpg" width="400">

## Video Results by Model B and Model C
Here we show a short gift instead of the actual videos.

- This is the result generated from Model B. Inputs are 2 videos.
<img src="https://github.com/richarduuz/Research_Project/blob/master/Model_B_Video_Gif.gif" width="400">

- This is the result generated from Model C. Inputs are a image and a video. 
<img src="https://github.com/richarduuz/Research_Project/blob/master/Model_C_Video_Gif.gif" width="400">

## What you can try
Feel free to give these models a try if you are interested. Simply click on the following links and try them on Colab. Remember to set the hardware accelerator in the notebook setting as GPU. More details are in directory of each model and their notebook. You don't need to train any model before trying them.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richarduuz/Research_Project/blob/master/ModelA/ModelA.ipynb) Try **Model A** in Colab Notebook to swap face from source image to target image

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richarduuz/Research_Project/blob/master/ModelB/ModelB.ipynb) Try **Model B** in Colab Notebook to swap face from source image to target image or from source video to target video

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richarduuz/Research_Project/blob/master/ModelC/ModelC.ipynb) Try **Model C** in Colab Notebook, the colab notebook only has the demo for swap face between two images. Other demo like video face swapping, training, server deployment can be seen in directory ModelC. You can download code and run them locally. The detailed description can be seen at README in ModelC directory.

The demo application is uploaded to present our work. You can download and install it. However it is not able to translate faces without server. We only turned on our server during our testing and presentation. Server code is uploaded as well. You may deploy it on your own and change server url to try this demo.

Please refer to each model directory for more detail and instruction.
