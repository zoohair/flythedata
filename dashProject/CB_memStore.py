from .server import dash, app, Output, Input, State, dcc, html, log

#data import
from . import dataModule

import numpy as np
import datetime

########################################
########################################

@app.callback(
    Output('stats','children'),
    [Input('xCfgLocations','data'),
     Input('xCfgAirlines', 'data'),
     Input('xCfgAircraft', 'data')]
    )
def updateText(xCfgLocations, xCfgAirlines, xCfgAircraft):
    selectedAirports   = xCfgLocations.get('airports', dataModule.Airports)
    selectedAirlines   = xCfgAirlines.get('airlines', dataModule.Airlines)
    selectedAircraft   = xCfgAircraft.get('aircraft', dataModule.Aircraft)

    filteredData = dataModule.filterData(selectedAirports, selectedAirlines, selectedAircraft)

    nAirports = len(np.unique(np.concatenate([filteredData['srcAirport'].values, filteredData['destAirport'].values])))
    nAirlines = filteredData['airline'].nunique()
    nAircraft = len(np.unique(np.concatenate([s.split(' ') for s in filteredData['aircraft'].values])))
    nFlights = len(filteredData)

    return [html.Div('%i Flights'%nFlights, className='timeWindow'),
            html.Div('%i Airports'%nAirports, className="timeWindow"),
            html.Div('%i Airlines'%nAirlines, className="timeWindow"),
            html.Div('%i Aircraft Types'%nAircraft, className="timeWindow"),
            ]



#######################################
#######################################

# @app.callback(
#     Output('xCfgAirlines', 'data'),
#     [Input('AirlinesGraph','selectedData')])
# def updateStore(selectedData):
#     log.warning('Not yet implemented')

#     return {}


########################################
########################################
@app.callback(
    Output('xCfgAircraft', 'data'),
    [Input('AircraftGraph', 'relayoutData')])
def updateStore(relayoutData):
########################################
########################################
    log.warning('Not yet implemented')

    return {}

########################################
########################################
@app.callback(
    Output('xCfgLocations', 'data'),
    [Input('WorldMapGraph', 'selectedData')])
def updateStore(locationSelected):
########################################
########################################
    log.warning('Not yet implemented')

    return {}


