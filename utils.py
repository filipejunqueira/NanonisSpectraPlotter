import numpy as np
import pandas as pd


def mask_nan(img: np.ndarray, nan_value=0):
    img = img.copy()
    img[np.isnan(img)] = nan_value
    return img


def build_spectra_hover(params_pandas: pd.DataFrame):
    hovertemplate = ""
    for i, col in enumerate(params_pandas.columns):
        hovertemplate += f"<b>{col}: </b>" + \
                         "%{customdata[" + f"{i}" + "]:,.3g}<br>"
    hovertemplate += '<extra></extra>'
    return hovertemplate


def build_dropdown_options(grid_dict, sxm):
    if sxm is None:
        sxm_channels = []
    else:
        sxm_channels = list(sxm.keys())

    all_channels = sxm_channels + grid_dict["fixed_parameters"] + grid_dict["experimental_parameters"]

    return [{"label": val, "value": val} for val in all_channels]