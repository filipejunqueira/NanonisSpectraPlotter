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


def dot3ds_2dict(grid: napy.read.Grid):
    out_dict = grid.header
    out_dict["basename"] = grid.basename
    for key, val in grid.signals.items():
        if val.ndim <= 2:
            out_dict[key] = val.ravel().tolist()
        else:
            out_dict[key] = val.reshape(-1, val.shape[-1]).tolist()

    return out_dict


def dot3ds_params2pd(dot3ds_data_dict):
    all_params = dot3ds_data_dict["fixed_parameters"] + dot3ds_data_dict["experimental_parameters"]
    data = np.array(dot3ds_data_dict["params"])
    df = pd.DataFrame(columns=all_params, data=data).dropna(axis=1, how="all")
    return df

