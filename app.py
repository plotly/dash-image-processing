import os
import base64
import time
import sys

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
from flask_caching import Cache


from utils import STORAGE_PLACEHOLDER, GRAPH_PLACEHOLDER
from utils import apply_filters, show_histogram, generate_lasso_mask, apply_enhancements

DEBUG = True

app = dash.Dash(__name__)
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'localhost:6379')
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)

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
            'Dash Image Processing App',
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
            html.Div(className='five columns', children=[
                drc.Card([
                    dcc.Upload(
                        id='upload-image',
                        children=[
                            'Drag and Drop or ',
                            html.A('Select an Image')
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

                    drc.NamedInlineRadioItems(
                        name='Selection Mode',
                        short='selection-mode',
                        options=[
                            {'label': 'Rectangular', 'value': 'select'},
                            {'label': 'Lasso', 'value': 'lasso'}
                        ],
                        val='select'
                    ),
                ]),

                drc.Card([
                    dcc.Dropdown(
                        id='dropdown-analyze',
                        options=[
                            {'label': 'Histogram', 'value': 'histogram'}
                        ],
                        searchable=False,
                        placeholder='Analyze...'
                    ),

                    dcc.Dropdown(
                        id='dropdown-filters',
                        options=[
                            {'label': 'Blur', 'value': 'blur'},
                            {'label': 'Contour', 'value': 'contour'},
                            {'label': 'Detail', 'value': 'detail'},
                            {'label': 'Enhance Edge', 'value': 'edge_enhance'},
                            {'label': 'Enhance Edge (More)', 'value': 'edge_enhance_more'},
                            {'label': 'Emboss', 'value': 'emboss'},
                            {'label': 'Find Edges', 'value': 'find_edges'},
                            {'label': 'Sharpen', 'value': 'sharpen'},
                            {'label': 'Smooth', 'value': 'smooth'},
                            {'label': 'Smooth (More)', 'value': 'smooth_more'}
                        ],
                        searchable=False,
                        placeholder='Basic Filter...'
                    ),

                    dcc.Dropdown(
                        id='dropdown-enhance',
                        options=[
                            {'label': 'Brightness', 'value': 'brightness'},
                            {'label': 'Color Balance', 'value': 'color'},
                            {'label': 'Contrast', 'value': 'contrast'},
                            {'label': 'Sharpness', 'value': 'sharpness'}
                        ],
                        searchable=False,
                        placeholder='Enhance...'
                    ),

                    html.Div(
                        id='div-enhancement-factor',
                        style={
                            'display': 'none',
                            'margin': '25px 5px 30px 0px'
                        },
                        children=[
                            f"Enhancement Factor:",
                            html.Div(
                                style={'margin-left': '5px'},
                                children=dcc.Slider(
                                    id='slider-enhancement-factor',
                                    min=0,
                                    max=2,
                                    step=0.1,
                                    value=1,
                                    updatemode='drag'
                                )
                            )
                        ]
                    ),

                    html.Button('Run Operation', id='button-run-operation')
                ]),

                html.Div(id='div-analysis-plot')
            ]),

            html.Div(className='seven columns', style={'float': 'right'}, children=[
                # The Interactive Image Div contains the dcc Graph showing the image, as well as the hidden div storing
                # the true image
                html.Div(
                    id='div-interactive-image',
                    children=[
                        GRAPH_PLACEHOLDER,
                        html.Div(
                            id='div-storage-image',
                            children=STORAGE_PLACEHOLDER,  # [Bytes, Filename, Image Size]
                            style={'display': 'none'}
                        )
                    ]
                )
            ])
        ])
    ])
])


@app.callback(Output('interactive-image', 'figure'),
              [Input('radio-selection-mode', 'value')],
              [State('interactive-image', 'figure')])
def update_selection_mode(selection_mode, figure):
    figure['layout']['dragmode'] = selection_mode
    return figure


@app.callback(Output('div-interactive-image', 'children'),
              [Input('upload-image', 'contents'),
               Input('button-run-operation', 'n_clicks')],
              [State('interactive-image', 'figure'),
               State('interactive-image', 'selectedData'),
               State('dropdown-filters', 'value'),
               State('dropdown-enhance', 'value'),
               State('slider-enhancement-factor', 'value'),
               State('upload-image', 'filename'),
               State('div-storage-image', 'children')])
def update_graph_interactive_image(content,
                                   n_clicks,
                                   figure,
                                   selectedData,
                                   filters,
                                   enhance,
                                   enhancement_factor,
                                   new_filename,
                                   storage):
    t1 = time.time()

    # Retrieve metadata stored in the storage
    filename = storage

    # If the file has changed (when a file is uploaded)
    if new_filename and new_filename != filename:
        if DEBUG:
            print(filename, "replaced by", new_filename)

        string = content.split(';base64,')[-1]
        im_pil = drc.b64_to_pil(string)

    # If the file HAS NOT changed (which means an operation was applied)
    else:
        # Retrieve the image stored inside the figure
        enc_str = figure['layout']['images'][0]['source'].split(';base64,')[-1]
        # Creates the PIL Image object from the b64 png encoding
        im_pil = drc.b64_to_pil(string=enc_str)
        im_size = im_pil.size

        # Select using Lasso
        if selectedData and 'lassoPoints' in selectedData:
            selection_mode = 'lasso'
            selection_zone = generate_lasso_mask(im_pil, selectedData)
        # Select using rectangular box
        elif selectedData and 'range' in selectedData:
            selection_mode = 'select'
            lower, upper = map(int, selectedData['range']['y'])
            left, right = map(int, selectedData['range']['x'])
            # Adjust height difference
            height = im_size[1]
            upper = height - upper
            lower = height - lower
            selection_zone = (left, upper, right, lower)
        # Select the whole image
        else:
            selection_mode = 'select'
            selection_zone = (0, 0) + im_size

        # If the filter dropdown was chosen, apply the filter selected by the user
        if filters:
            apply_filters(
                image=im_pil,
                zone=selection_zone,
                filter=filters,
                mode=selection_mode
            )

        if enhance:
            apply_enhancements(
                image=im_pil,
                zone=selection_zone,
                enhancement=enhance,
                enhancement_factor=enhancement_factor,
                mode=selection_mode
            )

    t2 = time.time()
    if DEBUG:
        print(f"Updated Image Storage in {t2-t1:.3f} sec")

    return [
        drc.InteractiveImagePIL(
            image_id='interactive-image',
            image=im_pil,
            enc_format='png',
            display_mode='fixed',
            verbose=DEBUG
        ),

        html.Div(
            id='div-storage-image',
            children=new_filename,
            style={'display': 'none'}
        )
    ]


@app.callback(Output('div-analysis-plot', 'children'),
              [Input('button-run-operation', 'n_clicks')],
              [State('dropdown-analyze', 'value'),
               State('interactive-image', 'figure')])
def show_analysis_plot(_, dropdown_analyze, figure):
    # Retrieve the image stored inside the figure
    enc_str = figure['layout']['images'][0]['source'].split(';base64,')[-1]
    # Creates the PIL Image object from the b64 png encoding
    im_pil = drc.b64_to_pil(string=enc_str)

    if dropdown_analyze == 'histogram':
        return show_histogram(im_pil)


@app.callback(Output('div-enhancement-factor', 'style'),
              [Input('dropdown-enhance', 'value')],
              [State('div-enhancement-factor', 'style')])
def show_slider_enhancement_factor(value, style):
    # If any enhancement is selected
    if value:
        style['display'] = 'block'
    else:
        style['display'] = 'none'

    return style


@app.callback(Output('dropdown-filters', 'value'),
              [Input('button-run-operation', 'n_clicks')])
def reset_dropdown_filters(_):
    return None


@app.callback(Output('dropdown-enhance', 'value'),
              [Input('button-run-operation', 'n_clicks')])
def reset_dropdown_enhance(_):
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
