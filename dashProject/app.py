from .server import app, log, plotlyConfig, dcc, html



#Import other helpful modules
import numpy as np
import pandas as pd
import uuid
import time
import os
import copy
import datetime
import grasia_dash_components as gdc
import dash_dangerously_set_inner_html

####################################
### Configuring default vars     ###
####################################
#Global variable is ok since it's not intended to be modified



header = html.Header([
            html.Div([
                html.Div('Fly The Data', className='logo'),
                html.H1('World Flight Routes',className='title'),
            ], className='title'),
            html.Div([
                html.A('About this dataset', href="#about"),
            ], className='links')
    ])

statsBar = html.Div([
            html.Div('Visualized:', className='label'),
            html.Div(id='stats', children=[
                html.Div('xx Flights', className='timeWindow'),
                html.Div('xx Airports', className='timeWindow'),
                html.Div('xx Airlines', className="timeWindow"),
                html.Div('xx Aircraft', className="timeWindow"),
            ])
        ],className="stats-bar")

#Dashboard container
bodyDivs = []


emptyFig = {'data':[], 'layout': {'xaxis':{'visible':False}, 'yaxis':{'visible':False}, 
                                  'paper_bgcolor':'rgba(0,0,0,0)', 'plot_bgcolor':'rgba(0,0,0,0)'}}

locationGraphConfig = copy.deepcopy(plotlyConfig)
locationGraphConfig['modeBarButtonsToRemove'] += ['autoScale2d']
location = html.Div([
            dcc.Graph(id='WorldMapGraph', config=locationGraphConfig, figure=emptyFig, 
                animate=True, clear_on_unhover=False, )
            ], className="location-wrapper")

airlineGraphConfig = copy.deepcopy(plotlyConfig)
airlineGraphConfig['displayModeBar'] = False
airlines = html.Div([
            dcc.Graph(id='AirlinesGraph', config=airlineGraphConfig, figure=emptyFig,
                     animate=False, clear_on_unhover=False)
            ], className="location-wrapper",style={'display': 'none'})

rangesGraphConfig = copy.deepcopy(plotlyConfig)
rangesGraphConfig['modeBarButtonsToRemove'] += ['autoScale2d']
ranges = html.Div([
            dcc.Graph(id='AircraftGraph', config=rangesGraphConfig, figure=emptyFig,
                    animate=False, clear_on_unhover=False)
            ], className="location-wrapper")

dashboard = html.Div([location, ranges],className='dashboard')

########################################
########################################

javaScripts = [gdc.Import(src='./assets/hoverCursor.js')]

bodyDivs += [header, statsBar, dashboard,
                dcc.Store(id='xCfgAirlines', data={}, storage_type='memory'),
                dcc.Store(id='xCfgLocations', data={},  storage_type='memory'),
                dcc.Store(id='xCfgAircraft', data={},  storage_type='memory')] + \
            javaScripts


app.layout = html.Article(bodyDivs)

from . import CB_memStore  
# from . import figCB_airlines
from . import figCB_location
from . import figCB_ranges


