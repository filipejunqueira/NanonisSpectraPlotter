# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from plotly.subplots import make_subplots
from plotly import graph_objects as go

from data import load_img
import plotly.express as px
import pandas as pd

from utils import mask_nan, conv_to_pillow

app = dash.Dash(__name__)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

sxm_fname = "C:\\Users\omicron_vt\\The University of Nottingham\\NottsNano - Instruments\\Unisoku LT\Results\\2021_12_13_TrainingWheelsOff\Au(111)_manipulation_1198.sxm"   #TODO replace this with upload component, eventually multiupload for dat spectra
sxm_data = load_img(sxm_fname)
sxm_channel = "Z"
sxm_trace_direction = "forward"
sxm_img = sxm_data[sxm_channel][sxm_trace_direction]

top_fig = make_subplots(rows=2, cols=2,
                        specs=[[{}, {}],
                               [{"colspan": 2}, None]],
                        column_widths=[0.5, 0.5]
                        )

# fig_sxm = px.imshow(mask_nan(sxm_img), color_continuous_scale="Gray").data[0]
# fig_spectra_pos_on_sxm = go.Figure()
# top_fig.add_trace(px.imshow(mask_nan(sxm_img), aspect="equal", color_continuous_scale="Gray").data[0], row=1, col=1)
# top_fig.add_trace(go.Image())
top_fig.add_trace(go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1]), row=1, col=1)
top_fig.add_layout_image(
            source=conv_to_pillow(mask_nan(sxm_img)),
            row=1,
            col=1,
            xref="x domain",
            yref="y domain",
            x=1,
            y=0,
            xanchor="right",
            yanchor="bottom",
            opacity=0.8,
            sizex=1,
            sizey=1,
            layer="below")


app.layout = html.Div(children=[
    html.H1(children='Spectra Explorer'),

    html.Div(children='''
        Hooray :).
    '''),

    dcc.Graph(
        id='ref-image',
        figure=top_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)