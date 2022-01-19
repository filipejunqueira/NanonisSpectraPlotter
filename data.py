import nanonispy as napy
import numpy as np
import pandas as pd
from PIL import Image
from nOmicron.utils.plotting import nanomap


def load_img(filename: str):
    return napy.read.Scan(filename).signals


def load_grid(filename: str):
    return napy.read.Grid(filename)


def sxm2pil(img: np.ndarray, min_cutoff=None, max_cutoff=None, cmap=nanomap):
    img = img.copy()

    if min_cutoff is None:
        min_cutoff = np.min(img)
    if max_cutoff is None:
        max_cutoff = np.max(img)

    normed_img = (img - min_cutoff) / (max_cutoff - min_cutoff)
    pillow_img = Image.fromarray(np.uint8(cmap(np.flipud(normed_img)) * 255))

    return pillow_img


def dot3ds_params2pd(grid: napy.read.Grid):
    all_params = grid.header["fixed_parameters"] + grid.header["experimental_parameters"]
    data_byteswapped = grid.signals["params"][0, :, :].byteswap().newbyteorder()    # odd bug
    df = pd.DataFrame(columns=all_params, data=data_byteswapped).dropna(axis=1, how="all")
    return df
