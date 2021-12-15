# !pip install -U torch torchvision
# !pip install git+https://github.com/facebookresearch/fvcore.git
# import torch, torchvision
# torch.__version__
# !git clone https://github.com/facebookresearch/detectron2 detectron2_repo
# !pip install -e detectron2_repo

# 1. Library imports
import uvicorn
from fastapi import FastAPI
from Table import Table
import numpy as np
import base64
import io
from PIL import Image
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import matplotlib.pyplot as plt
import numpy as np
import cv2

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import tensorflow as tf
import numpy as np
import base64
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from image_to_base64 import image_to_base64
from base64_to_image import base64_to_image
from detect_table import detect_table


# 2. Create the app object
app = FastAPI()
cfg = get_cfg()
cfg.merge_from_file("TB_X152.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.4  # set threshold for this model
cfg.MODEL.WEIGHTS = "TB_model_X152.pth"
cfg.MODEL.DEVICE = 'cpu'
predictor = DefaultPredictor(cfg)

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Table Detection': f'{name}'}

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def predict_Table(data:Table):
    data = data.dict()
    image64 = data['image64']
    try:
        return {
            'prediction': detect_table(image64,predictor)
        }
    except:
        return{
            'prediction':'not working'
        }

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload