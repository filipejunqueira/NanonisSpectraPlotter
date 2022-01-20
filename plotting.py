import numpy as np
from nOmicron.utils.plotting import nanomap
from plotly import graph_objects as go, express as px

from data import dot3ds_params2pd
from utils import build_spectra_hover, mpl_to_plotly


def make_image_plot():
    image_fig = go.Figure()
    image_fig.update_layout(title="Spectra Position",
                            width=600,
                            height=600,
                            autosize=True,
                            xaxis_title="x (m)",
                            yaxis_title="y (m)",
                            margin={'t': 100, 'b': 20, 'r': 20, 'l': 20})

    return image_fig


def make_spectra_fig():
    spectra_fig = go.Figure()
    spectra_fig.update_layout(title="Spectra",
                              xaxis_title="Sweep",
                              width=1200,
                              height=600,
                              margin={'t': 100, 'b': 20, 'r': 20, 'l': 20})

    return spectra_fig


def plot_positions_vs_image(dot3ds_data_dict, img):
    dot3ds_pandas = dot3ds_params2pd(dot3ds_data_dict)

    x_square = np.abs(
        (dot3ds_pandas["X (m)"].max() - dot3ds_pandas["X (m)"].min()) / (dot3ds_data_dict["dim_px"][0] - 1))
    y_square = np.abs(
        (dot3ds_pandas["Y (m)"].max() - dot3ds_pandas["Y (m)"].min()) / (dot3ds_data_dict["dim_px"][1] - 1))

    x_axis = np.linspace(dot3ds_pandas["X (m)"].min() - (x_square / 2),
                         dot3ds_pandas["X (m)"].max() + (x_square / 2),
                         dot3ds_data_dict["dim_px"][0])
    y_axis = np.linspace(dot3ds_pandas["Y (m)"].min() - (y_square / 2),
                         dot3ds_pandas["Y (m)"].max() + (y_square / 2),
                         dot3ds_data_dict["dim_px"][1])

    # Plotting
    image_fig = px.imshow(img, color_continuous_scale=mpl_to_plotly(nanomap), x=x_axis, y=y_axis,
                          origin="lower", aspect="equal")
    image_fig.add_trace(go.Scatter(x=dot3ds_pandas["X (m)"], y=dot3ds_pandas["Y (m)"], mode="markers",
                                   hoverinfo='text',
                                   text=dot3ds_pandas.columns,
                                   customdata=dot3ds_pandas.values,
                                   hovertemplate=build_spectra_hover(dot3ds_pandas)))

    image_fig.update_layout(title="Spectra Position",
                            width=600,
                            height=600,
                            autosize=True,
                            xaxis_title="x (m)",
                            yaxis_title="y (m)",
                            margin={'t': 100, 'b': 20, 'r': 20, 'l': 20})

    return image_fig


def plot_spectra(useful_data, selected_y_channels, dot3dsdata_dict):
    spectra_fig = make_spectra_fig()
    spectra_fig.data = []
    spectra_fig.update_layout(yaxis_title=selected_y_channels[0])

    all_y = np.zeros((len(useful_data) * len(selected_y_channels), len(dot3dsdata_dict["sweep_signal"])))
    all_y[:] = np.nan
    i = 0
    for pointindex, metadata in useful_data.items():
        for y_channel in selected_y_channels:
            all_y[i, :] = dot3dsdata_dict[y_channel][pointindex]
            spectra_fig.add_trace(go.Scatter(x=dot3dsdata_dict["sweep_signal"],
                                             y=dot3dsdata_dict[y_channel][pointindex],
                                             name=y_channel +
                                                  f": ({useful_data[pointindex]['x']:.2g}, "
                                                  f"{useful_data[pointindex]['y']:.2g})"))
            i += 1

    if i > 1:
        spectra_fig.add_trace(go.Scatter(x=dot3dsdata_dict["sweep_signal"],
                                         y=np.nanmean(all_y, axis=0),
                                         line=dict(width=4, dash="dash"),
                                         name="Mean"))

    return spectra_fig
