import os
import pandas as pd
import numpy as np
import dash
from PIL import Image
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash_image_components import pil_to_b64, HTML_IMG_SRC_PARAMETERS

RANGE = [0, 1]

app = dash.Dash(__name__)
server = app.server


# Custom Script for Heroku
if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


def display(im, new_width=500):
    ratio = new_width / im.size[0]
    new_height = round(im.size[1] * ratio)
    return im.resize((new_width, new_height))


im_pil = Image.open('images/IU2.jpg')
small_im = display(im_pil)


def InteractiveImage(id, im_pil):
    encoded_image = pil_to_b64(im_pil, enc_format='png')
    width, height = im_pil.size

    return dcc.Graph(
        id=id,
        figure={
            'data': [],
            'layout': {
                'margin': go.Margin(l=40, b=40, t=5, r=5),
                # 'width': '100%',
                'xaxis': {
                    'range': (0, width),
                    'scaleanchor': 'y'
                },
                'yaxis': {
                    'range': (0, height)
                },
                'autorange': False,
                'images': [{
                    'xref': 'x',
                    'yref': 'y',
                    'x': 0,
                    'y': 0,
                    'yanchor': 'bottom',
                    'sizex': width,
                    'sizey': height,
                    'layer': 'below',
                    'source': 'data:image/png;base64,{}'.format(encoded_image)
                }],
                'dragmode': 'select'  # or 'lasso'
            }
        }
    )

    # return dcc.Graph(
    #     id=id,
    #     figure={
    #         'data': [],
    #         'layout': {
    #             'margin': go.Margin(l=40, b=40, t=5, r=5),
    #             # 'width': '100%',
    #             'xaxis': {
    #                 'range': [0,1199]
    #             },
    #             'yaxis': {
    #                 'range': [0,778]
    #             },
    #             'images': [{
    #                 'xref': 'x',
    #                 'yref': 'y',
    #                 'x': 0,
    #                 'y': 0,
    #                 'yanchor': 'bottom',
    #                 'sizex': width,
    #                 'sizey': height,
    #                 'sizing': 'contain',
    #                 'layer': 'below',
    #                 'source': 'https://upload.wikimedia.org/wikipedia/commons/8/84/Rose-ringed_Parakeet_Psittacula_krameri_male_by_Dr._Raju_Kasambe_DSCN8937_%283%29.jpg'
    #             }],
    #             'dragmode': 'select'  # or 'lasso'
    #         }
    #     }
    # )


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
    html.Div([
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                html.Img(src=HTML_IMG_SRC_PARAMETERS + pil_to_b64(im_pil), width='100%')
            ]),

            html.Div(
                className='six columns',
                children=InteractiveImage('iu-img', im_pil)
            )
        ])

    ],
        className="container",
    )

])


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css"  # For production
]

for css in external_css:
    app.css.append_css({"external_url": css})

# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)