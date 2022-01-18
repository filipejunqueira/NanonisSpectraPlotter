import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
from nOmicron.utils.plotting import nanomap
import nanonispy as napy


def mask_nan(img: np.ndarray, nan_value=0):
    img = img.copy()
    img[np.isnan(img)] = nan_value
    return img


def conv_to_pillow(img: np.ndarray):
    img = img.copy()
    normed_img = (img - np.min(img)) / (np.max(img) - np.min(img))
    pillow_img = Image.fromarray(np.uint8(nanomap(normed_img) * 255))

    return pillow_img


def get_pos_from_grid(grid: napy.read.Grid):
    grid.signals