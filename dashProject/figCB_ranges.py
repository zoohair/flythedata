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
        if len(distances) < 100: continue
        groupLabels += [ac]
        rangeData += [distances]

        # if len(groupLabels) > 20: break


    fig = ff.create_distplot(rangeData, groupLabels, bin_size=100, show_hist = False, show_rug = False, histnorm='probability density') #density
    fig.layout['xaxis']['type'] = 'log'
    fig.layout['xaxis']['title'] = 'Distance (km)'

    fig.layout['yaxis']['title'] = 'Prob. Density'
    fig.layout['yaxis']['titlefont'] = {'color':'#a8a8a8'}

    fig.layout['title'] = 'Distances Flown'
    fig.layout['paper_bgcolor']='rgba(0,0,0,0)'
    fig.layout['plot_bgcolor']='rgba(0,0,0,0)'
    # fig.layout['margin']={'t': 40, 'b':20 , 'r':0, 'l': 50, 'pad': 1}
    fig.layout['font'] = {'color': '#fff',}
    fig.layout['hovermode'] = 'closest'

    fig.layout['legend']={'orientation':'v', 'xanchor': 'left', 'x': 1.2}

    #         titlefont = {
    #             'size': 16,
    #             'color': '#a8a8a8',
    #             'family': 'Open Sans'
    #             },            
    #         yaxis=dict(
    #             showgrid=True,
    #             gridcolor='rgba(255,255,255,.2)',
    #             showticklabels=True,
    #             ticks='',
    #             tickfont={'color':'white'},
    #             # dtick=1,#np.log10(50),
    #             type='log',
    #             visibile=True,
    #             title='Number of Individuals (Log)',
    #             titlefont={'color':'#a8a8a8'}
    #             ),
    #         font = {'color': '#fff',},
    #         xaxis  = {'range': [-.5,len(nSeen)-.5], 'visible':False},
    #         showlegend = False,
    #         legend={'orientation':'v'},
    #         hovermode = 'closest',
    #         autosize = False,
    #         paper_bgcolor='rgba(0,0,0,0)',
    #         plot_bgcolor='rgba(0,0,0,0)',
    #         margin={'t': 40, 'b':20 , 'r':0, 'l': 50, 'pad': 1},
    #         dragmode='select',
    #         clickmode='event+select',




    return fig

