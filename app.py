# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
from plotly import graph_objects as go
from plotly.subplots import make_subplots

import callbacks
from data import load_img, load_grid, dot3ds_2dict

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
load_figure_template(["darkly"])
app.title = "Spectra Explorer"

fig = go.Figure()

top_fig = make_subplots(rows=1, cols=1,
                        specs=[[{"secondary_y": True}]])
top_fig.update_layout(title="Spectra Position",
                      width=500,
                      height=500,
                      autosize=False,
                      template="darkly",
                      xaxis={'side': 'top'},
                      xaxis2={'anchor': 'y', 'overlaying': 'x', 'side': 'bottom'},
                      yaxis={'side': 'right'},
                      yaxis2={'side': 'left'},
                      margin={'t': 100, 'b': 20, 'r': 20, 'l': 5})
top_fig.layout.xaxis.update(showticklabels=False)
top_fig.layout.yaxis.update(showticklabels=False)

# top_fig.update_xaxes(matches='x2')
# top_fig.update_yaxes(matches='y2')

sxm_fname = "C:\\Users\omicron_vt\\The University of Nottingham\\NottsNano - Instruments\\Unisoku LT\Results\\2021_12_13_TrainingWheelsOff\Au(111)_manipulation_1198.sxm"  # TODO replace this with upload component, eventually multiupload for dat spectra
sxm_data = load_img(sxm_fname)
sxm_channel = "Z"
sxm_trace_direction = "forward"
sxm_img = sxm_data[sxm_channel][sxm_trace_direction]


@app.callback(Output('ref-image', 'figure'),
              Output('spectra-data', 'data'),
              Input("spectra-upload", 'value'))
def set_core_figs(spectra_path):
    if spectra_path is None:
        return top_fig, json.dumps("")

    dot3ds_data = load_grid(spectra_path)
    dot3ds_data_dict = dot3ds_2dict(dot3ds_data)

    updated_top_fig = top_fig
    # updated_top_fig = callbacks.set_title(updated_top_fig, dot3ds_data.basename)
    updated_top_fig = callbacks.plot_positions_vs_image(updated_top_fig, dot3ds_data_dict, sxm_img)

    return updated_top_fig, json.dumps(dot3ds_data_dict)


root_layout = html.Div([
    html.Div([
        dcc.Markdown("**Spectra: **",
                     style={'width': '100px', 'display': 'inline-block'}),
        dcc.Input(
            id="spectra-upload",
            type="text",
            persistence=True,
            debounce=True,
            style={'width': '400px'},
            placeholder=".3ds or .dat")]),
    html.Div([
        dcc.Markdown("**Optional sxm: **",
                     style={'width': '100px', 'display': 'inline-block'}),
        dcc.Input(
            id="sxm-upload",
            type="text",
            persistence=True,
            debounce=True,
            style={'width': '400px'},
            placeholder=".sxm")]),
    html.Div(
        dcc.Graph(
            id='ref-image',
            figure=top_fig)),
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
