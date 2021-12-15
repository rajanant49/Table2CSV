from PIL import Image
import numpy as np
import io
import base64

def base64_to_image(image64):
    # function to convert base64 string to image
    im = Image.open(io.BytesIO(base64.b64decode(image64)))
    im = np.array(im)
    return im