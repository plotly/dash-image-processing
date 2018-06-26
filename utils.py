import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_reusable_components as drc
from PIL import Image, ImageFilter


enc_str, im_size, im_mode = drc.pil_to_bytes_string(Image.open('images/default.jpg'))

STORAGE_PLACEHOLDER = ("default.jpg", str(im_size), im_mode)

GRAPH_PLACEHOLDER = drc.InteractiveImagePIL(
    image_id='interactive-image',
    image=Image.open('images/default.jpg'),
    enc_format='png',
    display_mode='fixed'
)

FILTER_OPTIONS = [
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
]

# Maps process name to the Image filter corresponding to that process
FILTERS_DICT = {
    'blur': ImageFilter.BLUR,
    'contour': ImageFilter.CONTOUR,
    'detail': ImageFilter.DETAIL,
    'edge_enhance': ImageFilter.EDGE_ENHANCE,
    'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
    'emboss': ImageFilter.EMBOSS,
    'find_edges': ImageFilter.FIND_EDGES,
    'sharpen': ImageFilter.SHARPEN,
    'smooth': ImageFilter.SMOOTH,
    'smooth_more': ImageFilter.SMOOTH_MORE
}


def apply_filters(image, zone, filter, mode='select'):
    filter_selected = FILTERS_DICT[filter]

    if mode == 'select':
        crop = image.crop(zone)
        crop_mod = crop.filter(filter_selected)
        image.paste(crop_mod, zone)

    elif mode == 'lasso':
        pass


def show_histogram(image):
    def hg_trace(name, color, hg):
        line = go.Scatter(
            x=list(range(0, 256)),
            y=hg,
            name=name,
            line=dict(color=(color)),
            mode='lines',
            showlegend=False
        )
        fill = go.Scatter(
            x=list(range(0, 256)),
            y=hg,
            mode='fill',
            name=name,
            line=dict(color=(color)),
            fill='tozeroy',
            hoverinfo='none'
        )

        return line, fill

    hg = image.histogram()

    if image.mode == 'RGBA':
        rhg = hg[0:256]
        ghg = hg[256:512]
        bhg = hg[512:768]
        ahg = hg[768:]

        data = [
            *hg_trace('Red', 'red', rhg),
            *hg_trace('Green', 'green', ghg),
            *hg_trace('Blue', 'blue', bhg),
            *hg_trace('Alpha', 'gray', ahg)
        ]

        layout = go.Layout(
            title='RGBA Histogram',
        )

    elif image.mode == 'RGB':
        # Returns a 768 member array with counts of R, G, B values
        rhg = hg[0:256]
        ghg = hg[256:512]
        bhg = hg[512:768]

        data = [*hg_trace('Red', 'red', rhg),
                *hg_trace('Green', 'green', ghg),
                *hg_trace('Blue', 'blue', bhg)]

        layout = go.Layout(
            title='RGB Histogram',
        )

    else:
        data = [*hg_trace('Gray', 'gray', rhg)]

        layout = go.Layout(
            title='Grayscale Histogram',
        )

    figure = go.Figure(data=data, layout=layout)

    return dcc.Graph(id='graph-histogram-colors', figure=figure)
