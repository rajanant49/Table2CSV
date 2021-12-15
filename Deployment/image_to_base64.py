from PIL import Image
import numpy as np
import io
import base64

def image_to_base64(image):
    # function to convert image to base64
    im = Image.fromarray(np.array(image))
    im_file = io.BytesIO()
    im.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    return im_b64