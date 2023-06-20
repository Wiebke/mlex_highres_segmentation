from dash import html, dcc
import dash_mantine_components as dmc

COMPONENT_STYLE = {
    "width": "640px",
    "height": "calc(100vh - 40px)",
    "padding": "10px",
    "borderRadius": "5px",
    "border": "1px solid rgb(222, 226, 230)",
    "overflowY": "auto",
}

FIGURE_CONFIG = {
    "modeBarButtonsToAdd": [
        "drawopenpath",
        "drawclosedpath",
        "eraseshape",
    ],
    "scrollZoom": True,
    "modeBarButtonsToRemove": [
        "zoom",
        "zoomin",
        "zoomout",
        "resetScale2d",
        "autoscale",
    ],
}


def layout():
    return html.Div(
        style=COMPONENT_STYLE,
        children=[
            dcc.Graph(id="image-viewer", config=FIGURE_CONFIG),
            dmc.Space(h=20),
            dmc.Slider(min=1, max=1000, step=1, value=25),
        ],
    )
