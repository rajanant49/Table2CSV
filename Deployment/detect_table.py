from PIL import Image
import cv2
import io
import base64
import numpy as np
import time
from base64_to_image import base64_to_image

def detect_table(image64,predictor):
  
  im = base64_to_image(image64)
  im = np.array(im)
  im = cv2.resize(im,(1024,1024))
  start_time = time.time()
  outputs = predictor(im)
  delta = time.time() - start_time
  print(delta)
  if len(outputs["instances"])>0:
    return True
  else:
    return False