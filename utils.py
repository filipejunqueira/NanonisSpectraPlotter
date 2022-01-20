import numpy as np
import pandas as pd
import nanonispy as napy
from data import sxm2dict


def mask_nan(img: np.ndarray, nan_value=0):
    img = img.copy()
    img[np.isnan(img)] = nan_value
    return img


def mpl_to_plotly(cmap, pl_entries=11, rdigits=2):
    scale = np.linspace(0, 1, pl_entries)
    colors = (cmap(scale)[:, :3]*255).astype(np.uint8)
    pl_colorscale = [[round(s, rdigits), f'rgb{tuple(color)}'] for s, color in zip(scale, colors)]
    return pl_colorscale


def build_spectra_hover(params_pandas: pd.DataFrame):
    hovertemplate = ""
    for i, col in enumerate(params_pandas.columns):
        hovertemplate += f"<b>{col}: </b>" + \
                         "%{customdata[" + f"{i}" + "]:,.3g}<br>"
    hovertemplate += '<extra></extra>'
    return hovertemplate


def build_dropdown_options(grid: napy.read.Grid, sxm: napy.read.Scan):
    if sxm is None:
        sxm_channels = []
    else:
        sxm_channels = list(sxm2dict(sxm).keys())

    grid_signal_channels = []
    for signal_channel, value in grid.signals.items():
        if signal_channel not in ["params", "sweep_signal"]:
            grid_signal_channels += [signal_channel]
    all_channels = grid_signal_channels + grid.header["fixed_parameters"] + grid.header["experimental_parameters"] + sxm_channels

    return [{"label": val, "value": val} for val in all_channels]

