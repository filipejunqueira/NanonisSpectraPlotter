import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
from nOmicron.utils.plotting import nanomap
import nanonispy as napy


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

