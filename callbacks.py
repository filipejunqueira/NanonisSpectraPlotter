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

    x_square = np.abs((dot3ds_pandas["X (m)"].max() - dot3ds_pandas["X (m)"].min()) / (dot3ds_data_dict["dim_px"][0] - 1))
    y_square = np.abs((dot3ds_pandas["Y (m)"].max() - dot3ds_pandas["Y (m)"].min()) / (dot3ds_data_dict["dim_px"][1] - 1))

    x_axis = np.linspace(dot3ds_pandas["X (m)"].min() - (x_square / 2),
                         dot3ds_pandas["X (m)"].max() + (x_square / 2),
                         dot3ds_data_dict["dim_px"][0])
    y_axis = np.linspace(dot3ds_pandas["Y (m)"].min() - (y_square / 2),
                         dot3ds_pandas["Y (m)"].max() + (y_square / 2),
                         dot3ds_data_dict["dim_px"][1])

    # Plotting
    top_fig = px.imshow(img, color_continuous_scale=mpl_to_plotly(nanomap), x=x_axis, y=y_axis,
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
