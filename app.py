# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json

import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly import express as px

import callbacks
from data import load_img, load_grid, dot3ds_2dict, sxm2dict
from utils import build_dropdown_options

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
# app._favicon = ("path_to_folder/(your_icon).co")
app.title = "Spectra Explorer"
load_figure_template(["darkly"])

top_fig = go.Figure()


spectra_fig = go.Figure()
spectra_fig.update_layout(title="Spectra",
                      width=1200,
                      height=600,
                      margin={'t': 100, 'b': 20, 'r': 20, 'l': 20})

@app.callback(Output('ref-image', 'figure'),
              Output('spectra-data', 'data'),
              Output('image-dropdown', 'options'),
              Input("spectra-upload", 'value'),
              Input('sxm-upload', 'value'),
              Input('image-dropdown', 'value'))
def set_core_figs(spectra_path, sxm_path, image_channel):
    if spectra_path is (None or ""):
        return top_fig, json.dumps(""), []

    dot3ds_data = load_grid(spectra_path)
    dot3ds_data_dict = dot3ds_2dict(dot3ds_data)

    if sxm_path is not (None or ""):
        sxm_data = load_img(sxm_path)
        sxm_data_dict = sxm2dict(sxm_data)
    else:
        sxm_data = None

    dropdown_opts = build_dropdown_options(dot3ds_data, sxm_data)

    if image_channel is None:
        return go.Figure(), json.dumps(dot3ds_data_dict), dropdown_opts
    elif image_channel in dot3ds_data_dict.keys():
        res = dot3ds_data.header["dim_px"]
        resizing = res + [-1]
        background_img = np.array(dot3ds_data_dict[image_channel]).reshape(resizing)[:, :,
                         0]  # for now slice it, replace with slider in future
    else:
        background_img = sxm_data_dict[image_channel]

    # updated_top_fig = callbacks.set_title(updated_top_fig, dot3ds_data.basename)
    updated_top_fig = callbacks.plot_positions_vs_image(dot3ds_data_dict, background_img)

    return updated_top_fig, json.dumps(dot3ds_data_dict), dropdown_opts


root_layout = html.Div([
    html.Hr(),
    html.Div([
        dcc.Markdown("** Spectra: **",
                     style={'width': '150px', 'display': 'inline-block'}),
        dcc.Input(
            id="spectra-upload",
            type="text",
            persistence=True,
            debounce=True,
            style={'width': '450px'},
            placeholder=".3ds or .dat")]),
    html.Div([
        dcc.Markdown("** Image (opt.): **",
                     style={'width': '150px', 'display': 'inline-block'}),
        dcc.Input(
            id="sxm-upload",
            type="text",
            persistence=True,
            debounce=True,
            style={'width': '450px'},
            placeholder=".sxm")]),
    html.Hr(),
    html.Div(
        dcc.Dropdown(id="image-dropdown",
                     style={'width': '600px'})),
    html.Hr(),
    html.Div([
        dcc.Graph(
            id='ref-image',
            figure=top_fig,
            style={'display': 'inline-block'}),
        dcc.Graph(
            id='ref-spectra',
            figure=spectra_fig,
            style={'display': 'inline-block'})
    ])
])

app.layout = dbc.Container(
    [root_layout,
     dcc.Store(id='spectra-data')],
    fluid=True,
    className="dbc"
)

# html.Label(["Select color bar "
#             "range:",
#             dcc.RangeSlider(
#                 id='colorbar-slider',
# min=0. max=10,
# tooltip={"placement": "bottom", "always_visible": True}
#             ), ])

if __name__ == '__main__':
    app.run_server(debug=True)
