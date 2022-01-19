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



