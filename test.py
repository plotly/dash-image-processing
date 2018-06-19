import os
import base64

import pandas as pd
import numpy as np
import json
import dash
from PIL import Image, ImageFilter
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_reusable_components as drc
import plotly.graph_objs as go

from dash_reusable_components import DisplayImagePIL, InteractiveImagePIL

RANGE = [0, 1]

app = dash.Dash(__name__)
server = app.server

im = Image.open('images/IU2.jpg')
imgSize = im.size
imb = im.tobytes()
enc_str = base64.b64encode(imb).decode('ascii')

dec = base64.b64decode(enc_str.encode('ascii'))
im_retrieved = Image.frombytes('RGB', imgSize, dec)

app.layout = html.Div([
    # Banner display
    html.Div([
        html.H2(
            'App Name',
            id='title'
        ),
        html.Img(
            src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"
        )
    ],
        className="banner"
    ),

    html.Div([
        InteractiveImagePIL(id='img1', image=im),

        InteractiveImagePIL(id='img2', image=im_retrieved)
    ])
])


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css"  # For production,
    # "https://rawgit.com/xhlulu/dash-image-display-experiments/master/custom_styles.css"  # For Development
]

for css in external_css:
    app.css.append_css({"external_url": css})

# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)
