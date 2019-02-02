import dash
from .server import app, Output, Input, State, dcc, html, log

#data import
from . import dataModule

import numpy as np

########################################
########################################
@app.callback(
    Output('AirlinesGraph', 'figure'),
    [Input('xCfgAircraft', 'data'), Input('xCfgLocations', 'data')],
    [State('xCfgAirlines', 'data')])
def genFigure(xCfgAircraft, xCfgLocations, xCfgAirlines):
########################################
########################################
    
    log.warning('not yet implemented!')
    raise dash.exceptions.PreventUpdate()

    # if xCfgDates == {} or xCfgLocations == {}:
    #     log.debug('Not ready to render Species Figure')
    #     raise dash.exceptions.PreventUpdate()

    # log.debug('Rendering Species Figure: TODO')

    # date_start, date_end = xCfgDates.get('dateRange', dataModule.dateRange)
    # selectedDiveSites = xCfgLocations.get('diveSites', dataModule.diveSites)

    # speciesList = dataModule.speciesList

    # selectedSpecies = xCfgSpecies.get('species', speciesList)

    # filteredData, _ = dataModule.filterData(date_start, date_end, 
    #                     speciesList, selectedDiveSites, 
    #                     'Site')


    # nSeen = [filteredData[s].sum() for s in speciesList]
    # text = ['%s: %i Sightings'%(s,n) for (s,n) in zip(speciesList, nSeen) ]
    # colors = [dataModule.colorLookup(s) for s in speciesList]
 

    # data = []
    # for (i, s, n, t, c) in zip(range(len(nSeen)), speciesList, nSeen, text, colors):
    #     if not (s in speciesList):
    #         c = 'rgba(0,0,0,0)'
    #         hoverinfo = 'none'
    #     else:
    #         hoverinfo = 'text'
    #     data += [dict(
    #         type = 'bar', #bar or barpolar
    #         x = [i],  y = [n],
    #         width=.9,
    #         name = s,
    #         text = [t],
    #         marker = {'color': c},
    #         hoverinfo=hoverinfo,
    #         orientation='v',
    #         customdata=[s],
    #         selectedpoints=[0] if s in selectedSpecies else [],
    #         )]


    #     layout = dict(
    #         uirevision=True,
    #         title = 'Species Frequency',
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

    #         updatemenus = getUpdateMenus(),
    #        )

    # fig = dict( data=data, layout=layout )

    # return fig
    

