import dash_reusable_components as drc
from PIL import Image, ImageFilter


PROCESS_OPTIONS = [
    {'label': 'Smooth', 'value': 'smooth'},
    {'label': 'Sharpen', 'value': 'sharpen'},
    {'label': 'Find Edges', 'value': 'find_edges'}
]

# Maps process name to the Image filter corresponding to that process
PROCESS_DICT = {
    'smooth': ImageFilter.SMOOTH,
    'sharpen': ImageFilter.SHARPEN,
    'find_edges': ImageFilter.FIND_EDGES
}


def apply_process(image, zone, process, mode='select'):
    if mode == 'select':
        filter_selected = PROCESS_DICT[process]
        crop = image.crop(zone)
        crop_mod = crop.filter(filter_selected)
        image.paste(crop_mod, zone)


enc_str, im_size, im_mode = drc.pil_to_bytes_string(Image.open('images/placeholder.png'))
STORAGE_PLACEHOLDER = (enc_str, "placeholder.png", str(im_size), im_mode)
