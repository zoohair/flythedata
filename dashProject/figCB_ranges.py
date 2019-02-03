import dash
from .server import app, Output, Input, State, dcc, html, log
import datetime

#data import
from . import dataModule

import numpy as np
import copy

import plotly.figure_factory as ff


########################################
########################################
@app.callback(
    Output('AircraftGraph', 'figure'),
    [Input('xCfgAirlines', 'data'), Input('xCfgLocations', 'data')],
    [State('xCfgAircraft', 'data')])
def genFigure(xCfgAirlines, xCfgLocations, xCfgAircraft):
########################################
########################################

    selectedAirports   = xCfgAirlines.get('airports', dataModule.Airports)
    selectedAirlines   = xCfgAirlines.get('airlines', dataModule.Airlines)
    selectedAircraft   = xCfgAircraft.get('aircraft', dataModule.Aircraft)

    routes = dataModule.filterData(selectedAirports, selectedAirlines, selectedAircraft)


    # YlOrRd = cl.scales['9']['seq']['YlOrRd']
    # clrscale = cl.to_rgb(cl.interp( YlOrRd, 10 ))


    rangeData = []
    groupLabels = []
    for ac, df in routes.groupby('aircraft'):
        distances = df['distance'].values
        if len(distances) < 10: continue
        ac = ac.replace('Boeing ', 'B').replace('Airbus ', '').replace('McDonnell Douglas ', '').replace('Embraer ', 'E').replace('Aerospatiale/Alenia ','')
        groupLabels += [ac[0:20]] #max 20 characters
        rangeData += [distances/np.mean(distances)]

    fig = ff.create_distplot(rangeData, groupLabels, 
                bin_size=100, show_hist = False, show_rug = False, histnorm='probability') #density
    
    for d in fig['data']:
        d['opacity'] = 0.6


    fig.layout['xaxis']['type'] = 'log'
    fig = fig.to_dict()

    fig['layout'].update(  dict(
            title = 'Distances Flown by Aircraft Type',
            titlefont = {
                'size': 16,
                'color': '#a8a8a8',
                'family': 'Open Sans'
                },
            font = {'color': '#fff',},
            xaxis = dict(
                type='log',
                showgrid=True,
                gridcolor='rgba(255,255,255,.2)',
                tickfont={'color':'white'},
                title= 'Normalized Distance', 
                titlefont= {'color': '#a8a8a8'}),
            yaxis=dict(
                showgrid=False,
                showticklabels=True,
                ticks='',
                tickfont={'color':'white'},
                visibile=True,
                title= 'Prob. Density', 
                titlefont={'color':'#a8a8a8'}
                ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin={'t': 40, 'b':40 , 'r':0, 'l': 50, 'pad': 1},
            legend={'orientation':'v', 'xanchor': 'left', 'x': 1},
            ))


    return fig

