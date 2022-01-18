import numpy as np


def mask_nan(img, nan_value=0):
    img = img.copy()
    img[np.isnan(img)] = nan_value
    return img
