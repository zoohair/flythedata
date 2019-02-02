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

    nAirports = filteredData['srcAirport'].nunique()
    nAirlines = filteredData['airlineIATA'].nunique()
    nAircraft = filteredData['aircraft'].nunique()

    return [html.Div('%i Airports'%nAirports, className='timeWindow'),
            html.Div('%i Airlines'%nAirlines, className="timeWindow"),
            html.Div('%i Aircraft'%nAircraft, className="timeWindow"),
            ]



#######################################
#######################################

@app.callback(
    Output('xCfgAirlines', 'data'),
    [Input('AirlinesGraph','selectedData')])
def updateStore(selectedData):
    log.warning('Not yet implemented')

    return {}


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

