# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_bootstrap_templates import load_figure_template
from plotly import graph_objects as go, express as px
from plotly.subplots import make_subplots
import numpy as np

from data import load_img, sxm2pil, dot3ds_params2pd, load_grid
from utils import mask_nan, build_spectra_hover

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
load_figure_template(["darkly"])
app.title = "Spectra Explorer"

sxm_fname = "C:\\Users\omicron_vt\\The University of Nottingham\\NottsNano - Instruments\\Unisoku LT\Results\\2021_12_13_TrainingWheelsOff\Au(111)_manipulation_1198.sxm"  # TODO replace this with upload component, eventually multiupload for dat spectra
sxm_data = load_img(sxm_fname)
sxm_channel = "Z"
sxm_trace_direction = "forward"
sxm_img = sxm_data[sxm_channel][sxm_trace_direction]

dot3ds_fname = "C:\\Users\omicron_vt\The University of Nottingham\\NottsNano - Instruments\\Unisoku LT\Results\\2021_12_13_TrainingWheelsOff\AnotherAtomDepositionAttempt_046.3ds"
dot3ds_data = load_grid(dot3ds_fname)
dot3ds_pandas = dot3ds_params2pd(dot3ds_data)

hovertemplate = build_spectra_hover(dot3ds_pandas)

top_fig = make_subplots(rows=1, cols=2,
                        specs=[[{"secondary_y": True}, {"secondary_y": False}]])

top_fig.update_layout(title="filename",
                      width=700,
                      height=350,
                      autosize=False,
                      template="darkly",
                      xaxis={'side': 'top'},
                      xaxis2={'anchor': 'y', 'overlaying': 'x', 'side': 'bottom'},
                      yaxis={'side': 'right'},
                      yaxis2={'side': 'left'})

top_fig.add_trace(px.imshow(sxm2pil(mask_nan(sxm_img))).data[0],
                  secondary_y=False, row=1, col=1)

top_fig.add_trace(go.Scatter(x=dot3ds_pandas["X (m)"].round(12), y=dot3ds_pandas["Z (m)"].round(12), mode="markers",
                             hoverinfo='text',
                             text=dot3ds_pandas.columns,
                             customdata=dot3ds_pandas.values,
                             hovertemplate=hovertemplate), secondary_y=True, row=1, col=1)

top_fig.data[1].update(xaxis='x2')
top_fig.layout.xaxis.update(showticklabels=False)
top_fig.layout.yaxis.update(showticklabels=False)
# top_fig.update_xaxes(matches='x2')
# top_fig.update_yaxes(matches='y2')

root_layout = html.Div(children=[
    dcc.Upload(
        id='upload-sxm-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a .sxm File')
        ]),
        style={
            'width': '680px',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'display': 'inline-block'
        }
    ),
    dcc.Graph(
        id='ref-image',
        figure=top_fig
    )
])

app.layout = dbc.Container(
    [root_layout],
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
