import base64
from io import BytesIO as _BytesIO

import dash_core_components as dcc
import dash_html_components as html
import numpy as np

import plotly.graph_objs as go
from PIL import Image


# Variables
HTML_IMG_SRC_PARAMETERS = 'data:image/png;base64, '


# Display utility functions
def _merge(a, b):
    return dict(a, **b)


def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


# Image utility functions
def pil_to_b64(im, enc_format='png'):
    """
    Converts a PIL Image into base64 string for HTML displaying
    :param im: PIL Image object
    :param enc_format: The image format for displaying. If saved the image will have that extension.
    :return: base64 encoding
    """
    buff = _BytesIO()
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
    buffer = _BytesIO(decoded)
    im = Image.open(buffer)

    return im


def b64_to_numpy(string, to_scalar=True):
    im = b64_to_pil(string)
    np_array = np.asarray(im)

    if to_scalar:
        np_array = np_array / 255.

    return np_array


# Custom Display Components
def Card(children, **kwargs):
    return html.Section(
        children,
        style=_merge({
            'padding': 20,
            'margin': 5,
            'borderRadius': 5,
            'border': 'thin lightgrey solid',

            # Remove possibility to select the text for better UX
            'user-select': 'none',
            '-moz-user-select': 'none',
            '-webkit-user-select': 'none',
            '-ms-user-select': 'none'
        }, kwargs.get('style', {})),
        **_omit(['style'], kwargs)
    )


def NamedSlider(name, short, min, max, step, val, marks=None):
    if marks:
        step = None
    else:
        marks = {i: i for i in range(min, max + 1, step)}

    return html.Div(
        style={'margin': '25px 5px 30px 0px'},
        children=[
            f"{name}:",

            html.Div(
                style={'margin-left': '5px'},
                children=dcc.Slider(
                    id=f'slider-{short}',
                    min=min,
                    max=max,
                    marks=marks,
                    step=step,
                    value=val
                )
            )
        ]
    )


def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f'div-{short}',
        style=_merge({
            'display': 'inline-block'
        }, kwargs.get('style', {})),
        children=[
            f'{name}:',
            dcc.RadioItems(
                id=f'radio-{short}',
                options=options,
                value=val,
                labelStyle={
                    'display': 'inline-block',
                    'margin-right': '7px',
                    'font-weight': 300
                },
                style={
                    'display': 'inline-block',
                    'margin-left': '7px'
                }
            )
        ],
        **_omit(['style'], kwargs)
    )


# Custom Image Components
def InteractiveImagePIL(id, image, enc_format='png', **kwargs):
    encoded_image = pil_to_b64(image, enc_format=enc_format)
    width, height = image.size
    display_height = '{}vw'.format(round(60 * height / width))

    return dcc.Graph(
        id=f'graph-{id}',
        figure={
            'data': [],
            'layout': {
                'margin': go.Margin(l=40, b=40, t=26, r=10),
                'xaxis': {
                    'range': (0, width),
                    'scaleanchor': 'y',
                    'scaleratio': 1
                },
                'yaxis': {
                    'range': (0, height)
                },
                'images': [{
                    'xref': 'x',
                    'yref': 'y',
                    'x': 0,
                    'y': 0,
                    'yanchor': 'bottom',
                    'sizing': 'stretch',
                    'sizex': width,
                    'sizey': height,
                    'layer': 'below',
                    'source': HTML_IMG_SRC_PARAMETERS + encoded_image,
                }],
                'dragmode': 'lasso',
            }
        },
        style=_merge({
            'height': display_height,
        }, kwargs.get('style', {})),
        config={
            'modeBarButtonsToRemove': [
                'sendDataToCloud',
                'autoScale2d',
                'toggleSpikelines',
                'hoverClosestCartesian',
                'hoverCompareCartesian'
            ]
        },
        **_omit(['style'], kwargs)
    )


def DisplayImagePIL(id, image, **kwargs):
    encoded_image = pil_to_b64(image, enc_format='png')

    return html.Img(
        id=f'img-{id}',
        src=HTML_IMG_SRC_PARAMETERS + encoded_image,
        width='100%',
        **kwargs
    )

