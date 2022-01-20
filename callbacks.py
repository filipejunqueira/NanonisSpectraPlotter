from plotly import graph_objects as go, express as px

from data import sxm2pil, dot3ds_params2pd
from utils import mask_nan, build_spectra_hover


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


def plot_positions_vs_image(top_fig, dot3ds_data, sxm_img):
    dot3ds_pandas = dot3ds_params2pd(dot3ds_data)

    top_fig.data = []
    top_fig.add_trace(px.imshow(sxm2pil(mask_nan(sxm_img))).data[0],
                      secondary_y=False, row=1, col=1)
    top_fig.add_trace(go.Scatter(x=dot3ds_pandas["X (m)"].round(12), y=dot3ds_pandas["Z (m)"].round(12), mode="markers",
                                 hoverinfo='text',
                                 text=dot3ds_pandas.columns,
                                 customdata=dot3ds_pandas.values,
                                 hovertemplate=build_spectra_hover(dot3ds_pandas)), secondary_y=True, row=1, col=1)
    top_fig.data[1].update(xaxis='x2')

    return top_fig
