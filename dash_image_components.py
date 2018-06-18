import base64
from io import BytesIO

import numpy as np
from PIL import Image


IM_FORMAT = b'png'
HTML_IMG_SRC_PARAMETERS = b'data:image/' + IM_FORMAT + b';base64'


def pil_to_b64(im, enc_format='png'):
    """
    Converts a PIL Image into base64 string for HTML displaying
    :param im: PIL Image object
    :param enc_format: The image format for displaying. If saved the image will have that extension.
    :return: base64 encoding
    """
    buff = BytesIO()
    im.save(buff, format=enc_format)
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

    return encoded


def numpy_to_b64(np_array, enc_format='png', scalar=True):
    """
    Converts a numpy image into base 64 string for HTML displaying
    :param np_array:
    :param enc_format: The image format for displaying. If saved the image will have that extension.
    :param scalar:
    :return:
    """
    # Convert from 0-1 to 0-255
    if scalar:
        np_array = np.uint8(255 * np_array)
    else:
        np_array = np.uint8(np_array)

    im_pil = Image.fromarray(np_array)

    return pil_to_b64(im_pil, enc_format)


def b64_to_pil(string):
    decoded = base64.b64decode(string)
    buffer = BytesIO(decoded)
    im = Image.open(buffer)

    return im


def b64_to_numpy(string, to_scalar=True):
    im = b64_to_pil(string)
    np_array = np.asarray(im)

    if to_scalar:
        np_array /= 255.

    return np_array


if __name__ == '__main__':
    # Cycle Consistency
    pass
