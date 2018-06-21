import dash_reusable_components as drc
from PIL import Image, ImageFilter


enc_str, im_size, im_mode = drc.pil_to_bytes_string(Image.open('images/placeholder.png'))

STORAGE_PLACEHOLDER = (enc_str, "placeholder.png", str(im_size), im_mode)

GRAPH_PLACEHOLDER = drc.InteractiveImagePIL(
    image_id='interactive-image',
    image=Image.open('images/placeholder.png'),
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