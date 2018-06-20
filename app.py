import os
import base64
import time

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

RANGE = [0, 1]

app = dash.Dash(__name__)
server = app.server

# Custom Script for Heroku
if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

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

    # Body
    html.Div(className="container", children=[
        html.Div(className='row', children=[
            html.Div(className='four columns', children=drc.Card([
                dcc.Upload(
                    id='upload-image',
                    children=[
                        'Drag and Drop or ',
                        html.A('Select a File')
                    ],
                    style={
                        'width': '100%',
                        'height': '50px',
                        'lineHeight': '50px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                    },

                    accept='image/*'
                ),

                html.Div(
                    id='div-storage-image',
                    children=[None, None, None],  # [Bytes, Filename, Image Size]
                    style={'display': 'none'}
                ),

                dcc.Dropdown(
                    id='dropdown-process',
                    options=[
                        {'label': 'Smooth', 'value': 'smooth'},
                        {'label': 'Sharpen', 'value': 'sharpen'},
                        {'label': 'Find Edges', 'value': 'find_edges'}
                    ],
                    searchable=False,
                    placeholder='Process'
                ),
                html.Button('Submit', id='button')

            ])),

            html.Div(className='eight columns', children=[
                html.Div(id='div-interactive-image'),

                html.Div(id='div-image-json'),
            ])
        ])
    ])
])


@app.callback(Output('div-storage-image', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('div-storage-image', 'children')])
def update_image_storage(content, filename, old_storage):
    # If filename has changed
    old_filename = old_storage[1]
    print(old_filename, "replaced by", filename)

    # If the file has changed (when user uploads something)
    if filename != old_filename:
        extension = filename.split('.')[-1].lower()

        t1 = time.time()

        string = content.split(';base64,')[-1]
        im_pil = drc.b64_to_pil(string)
        im_bytes = im_pil.tobytes()
        enc_str = base64.b64encode(im_bytes).decode('ascii')
        im_size = im_pil.size

        t2 = time.time()
        print(f"Updated Image Storage in {t2-t1:.2f} sec")

        return [enc_str, filename, str(im_size)]

    return old_storage


@app.callback(Output('div-interactive-image', 'children'),
              [Input('div-storage-image', 'children')])
def update_interactive_image(children):
    if all(children):
        t1 = time.time()
        enc_str, filename, im_size = children
        im_size = eval(im_size)

        decoded = base64.b64decode(enc_str.encode('ascii'))
        im_pil = Image.frombytes('RGB', im_size, decoded)

        t2 = time.time()
        print(f"Decoded interactive image in {t2-t1:.2f} sec")

        return drc.InteractiveImagePIL(
            image_id='interactive-image',
            image=im_pil
        )
    else:
        return None


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
