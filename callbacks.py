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


def plot_positions_vs_image(dot3ds_data_dict, img):
    dot3ds_pandas = dot3ds_params2pd(dot3ds_data_dict)

    centre = dot3ds_data_dict["pos_xy"]
    size = dot3ds_data_dict["size_xy"]

    x_axis = np.linspace(centre[0] - size[0] / 2, centre[0] + size[0] / 2, img.shape[0])
    y_axis = np.linspace(centre[1] - size[1] / 2, centre[1] + size[1] / 2, img.shape[1])

    # Plotting
    top_fig = px.imshow(np.rot90(img), color_continuous_scale=mpl_to_plotly(nanomap), x=x_axis, y=y_axis,
                        origin="lower", aspect="equal")
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
                          margin={'t': 100, 'b': 20, 'r': 20, 'l': 20})

    return top_fig
