import numpy as np
from nOmicron.utils.plotting import nanomap
from plotly import graph_objects as go, express as px

from data import dot3ds_params2pd
from utils import build_spectra_hover, mpl_to_plotly


def set_title(top_fig, filename):
    if filename is None:
        top_fig.update_layout(title="Waiting...")
    elif ".3ds" in filename:
        top_fig.update_layout(title=filename)
    elif ".dat" in filename:
        top_fig.update_layout(title=filename)
    else:
        top_fig.update_layout(title="Unsuppprted File")

    return top_fig


def plot_positions_vs_image(dot3ds_data_dict, sxm_img):
    x_axis = np.linspace(dot3ds_data_dict["pos_xy"][0],
                         dot3ds_data_dict["pos_xy"][0] + dot3ds_data_dict["size_xy"][0],
                         sxm_img.shape[0]) - (dot3ds_data_dict["size_xy"][0] / 2)
    y_axis = np.linspace(dot3ds_data_dict["pos_xy"][1],
                         dot3ds_data_dict["pos_xy"][1] + dot3ds_data_dict["size_xy"][1],
                         sxm_img.shape[1]) - (dot3ds_data_dict["size_xy"][1] / 2)
    dot3ds_pandas = dot3ds_params2pd(dot3ds_data_dict)

    top_fig = px.imshow(sxm_img, color_continuous_scale=mpl_to_plotly(nanomap), x=x_axis, y=y_axis)
    top_fig.add_trace(go.Scatter(x=dot3ds_pandas["X (m)"], y=dot3ds_pandas["Y (m)"], mode="markers",
                                 hoverinfo='text',
                                 text=dot3ds_pandas.columns,
                                 customdata=dot3ds_pandas.values,
                                 hovertemplate=build_spectra_hover(dot3ds_pandas)))

    top_fig.update_layout(title="Spectra Position",
                          width=600,
                          height=600,
                          autosize=True,
                          template="darkly",
                          xaxis={'side': 'top'},
                          xaxis2={'anchor': 'y', 'overlaying': 'x', 'side': 'bottom'},
                          yaxis={'side': 'right'},
                          yaxis2={'side': 'left'},
                          margin={'t': 100, 'b': 20, 'r': 20, 'l': 20})

    return top_fig
