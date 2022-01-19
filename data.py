import nanonispy as napy
import numpy as np
import pandas as pd
from PIL import Image
from nOmicron.utils.plotting import nanomap


def load_img(filename: str):
    return napy.read.Scan(filename).signals


def load_grid(filename: str):
    return napy.read.Grid(filename)


def sxm2pil(img: np.ndarray):
    img = img.copy()
    normed_img = (img - np.min(img)) / (np.max(img) - np.min(img))
    pillow_img = Image.fromarray(np.uint8(nanomap(normed_img) * 255))

    return pillow_img


def dot3ds_params2pd(grid: napy.read.Grid):
    all_params = grid.header["fixed_parameters"] + grid.header["experimental_parameters"]
    return pd.DataFrame(columns=all_params, data=grid.signals["params"][0,:,:])
