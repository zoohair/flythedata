import dash
from .server import app, Output, Input, State, dcc, html, log
import datetime

#data import
from . import dataModule

import numpy as np
import copy


########################################
########################################
@app.callback(
    Output('AircraftGraph', 'figure'),
    [Input('xCfgAirlines', 'data'), Input('xCfgLocations', 'data')],
    [State('xCfgAircraft', 'data')])
def genFigure(xCfgAirlines, xCfgLocations, xCfgAircraft):
########################################
########################################

    log.warning('not yet implemented!')
    raise dash.exceptions.PreventUpdate()