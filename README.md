# Table2CSV
This repository contains code and knwledge gathered during my 1 month internship with FinsightAI Technologies.

# Table Identifiction using TableNet
* The data used was [FinTabNet](https://developer.ibm.com/exchanges/data/all/fintabnet/). This dataset contains complex tables from the annual reports of S&P 500 companies with detailed table structure annotations to help train and test structure recognition. Tables are split as Train – 91596, Test – 10656 and Val – 10635.
* I used the Val set to trainand test the model.
* The model architechture used for Image segmentation was TableNet. 

### TableNet ([Paper](https://arxiv.org/abs/2001.01469)) ([Explanation Blog](https://medium.com/analytics-vidhya/tablenet-deep-learning-model-for-end-to-end-table-detection-and-tabular-data-extraction-from-1961fb2f97e1))- 

TableNet is a modern deep learning architecture that was proposed by a team from TCS Research year in the year 2019. The main motivation was to extract information from scanned tables through mobile phones or cameras.

![im1](https://user-images.githubusercontent.com/77537478/115711117-c6bfaa80-a390-11eb-80a4-7842e3531f03.JPG)

Architecture: The architecture is based out of Long et al., an encoder-decoder model for semantic segmentation. The same encoder/decoder network is used as the FCN architecture for table extraction. The images are preprocessed and modified using the Tesseract OCR. It is the pixel-wise detection of tabular sub-image while tabular structure recognition involves segmentation of the individual rows and columns in the detected table. The model consists of two parts which are encoder and decoder. The pre-trained VGG19 model is introduced as the baseline encoder model.

Some results - 


# Table Detection Using Faster-RCNN 
* Data used - TableBank
([Git-Repo](https://github.com/doc-analysis/TableBank)) & FinTabNet<br>

* We use the open-source framework Detectron2 to train models on the TableBank. Detectron2 is a high-quality and high-performance codebase for object detection research, which supports many state-of-the-art algorithms. In this task, we use the Faster R-CNN algorithm with the ResNeXt as the backbone network architecture, where the parameters are pre-trained on the ImageNet dataset. 
* Pretrained Model on TableBank was used and fintuned on Fintabnet dataset. The TableBank containes data related to mostly Bordered Tables whereas FinTabNet contains mainly borderless type table . 

Some Results - 

# Deployment using FastAPI
* FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
* The app simply takes an base64 image string as input and returns whether a table is present in the image or not using the object detection model trained earlier.

# Conversion of Table to CSV
* This task is handled by [AWS Textract](https://aws.amazon.com/textract/) , which is capable of recognizing the tabular structure in an image as well as extraction of the tabular data into json format . 
* The json file recieved is then manipulated using custom functions to convert into a csv file . 

Some Results - 






