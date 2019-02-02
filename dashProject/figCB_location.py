import dash
from .server import app, Output, Input, State, dcc, html, log, mapboxtoken

import numpy as np
import datetime

#data import
from . import dataModule

#TODO: use xsrc and ysrc to avoid duplicating data?

########################################
########################################
@app.callback(
    Output('WorldMapGraph', 'figure'),
    [Input('xCfgAircraft', 'data'), Input('xCfgAirlines', 'data')])
def genLocationFigure(xCfgAircraft, xCfgAirlines):
########################################
########################################
   
    log.warning('not yet implemented!')
    raise dash.exceptions.PreventUpdate()



    # date_start, date_end = xCfgDates.get('dateRange', dataModule.dateRange)
    # if isinstance(date_start, str): date_start = datetime.datetime.fromisoformat(date_start).date()
    # if isinstance(date_end, str):   date_end   = datetime.datetime.fromisoformat(date_end).date()

    # selectedSpecies      = xCfgSpecies.get('species', dataModule.speciesList)

    # selectedDiveSites = dataModule.diveSites

    # filteredData, _ = dataModule.filterData(date_start, date_end, 
    #                         selectedSpecies, selectedDiveSites, 
    #                         'Site')

    # mWeeks = dataModule.daysWithData(date_start, date_end)/7.

    # refSize = 100
    # minSize = 5

    # def hasSighting(row): 
    #     try:
    #         return np.any([row[s] > 0 for s in selectedSpecies])
    #     except:
    #         print([row[s] for s in selectedSpecies])
    #         return False

    # def safe_div(x,y):
    #     try: return x/y
    #     except ZeroDivisionError: return 0
    # ##################
    # #Dive Effort Data
    # ##################
    # xArr   = []
    # yArr   = []
    
    # diveCountTxt = []
    # sightingsTxt = []

    # diveSizes = []
    # sightingSizes = []
    # sightingsRate = []
    # #For each dive site, we will compute the number of dives
    # #and number of sightings 
    # for d in selectedDiveSites:
    #     #Get location of Dive Site
    #     xyLoc = diveSiteLoc(d)
    #     xArr += [xyLoc[0] + 0*11.4]
    #     yArr += [xyLoc[1] + 0*26.4]  

    #     #filter dives sites of interest
    #     idx = filteredData['Site'] == d
    #     subfData = filteredData[idx]

    #     #Number of dives is just how many rows we have 
    #     nDives = len(subfData.index)

    #     divesPerWeek = safe_div(nDives, mWeeks)
    #     diveSizes += [refSize*nDives]

    #     #Count number of dives which had a sighting of the selected species!
    #     if nDives > 0:
    #         nSightings = np.sum(subfData.apply(hasSighting,axis=1))
    #     else:
    #         nSightings = 0

    #     sightingsRate += [safe_div(nSightings,nDives)]
        

    #     diveCountTxt += ['%s:<br>~%.1f dive/week (%i dives in %i week[s])<br>'\
    #                      '~%.1f sighting/week (sightings in %.0f%% of dives)'%
    #                     (d,divesPerWeek,nDives,mWeeks,
    #                     safe_div(nSightings, mWeeks),sightingsRate[-1]*100)]

    #     sightingsTxt += [diveCountTxt[-1]]


    # diveSizes = np.array(diveSizes) / np.max(diveSizes) * refSize
    # sightingSizes = np.sqrt(np.array(sightingsRate)) * diveSizes

    # #Legend Entry
    # # xArr += [-10]
    # # yArr += [10]
    # # diveCountTxt += ['']
    # # sightingsTxt += ['']
    # # diveSizes += [30]
    # # sightingSizes += [20]

    # customdata = [d for d in selectedDiveSites] + ['']

    # #dive effort
    # data = [dict(
    #     type='scattermapbox',
    #     mode = 'markers',
    #     lon = xArr, lat = yArr,
    #     selectgroup=list(range(len(xArr))),
    #     customdata = customdata,
    #     # text = diveCountTxt,
    #     hoverinfo='none',
    #     marker= {'size': diveSizes, 'sizemin': minSize,
    #              'color':'rgb(0,0,0)', #nofill for this marker
    #              'line': {'width': 1, 'color': '#ffffff'},
    #              'opacity': 0.1},
    #     )]

    # #sightings
    # data +=[dict(
    #     type='scattermapbox',
    #     mode = 'markers',
    #     lon = xArr, lat = yArr,
    #     selectgroup=list(range(len(xArr))),
    #     customdata = customdata,
    #     # text = sightingsTxt,
    #     hoverinfo='none',
    #     marker= {'size': sightingSizes,
    #              'color':'#f47d57', 'opacity': .55,
    #              'line': {'width': 0, 'color': 'rgba(0,0,0,0)'}},
    #     )]


    # locationColors = ['#ffde6d' if s > 0 else 'gray' for s in sightingSizes]
    # #Locations
    # data += [dict(
    #     type='scattermapbox',
    #     mode='markers',
    #     lon = xArr, lat = yArr,
    #     selectgroup=list(range(len(xArr))),
    #     customdata = customdata,
    #     hoverinfo ='text',
    #     text = sightingsTxt,
    #     marker={'color': locationColors,  'size': 4, 'line':{'width':0}},
    #     )]

    # #Legend
    # data += [
    #     dict(
    #         type='scattermapbox',
    #         mode='markers+text',
    #         lon = [10], lat = [27.5],
    #         text = 'Tofo',
    #         textposition = 'middle right',
    #         hoverinfo = 'none',
    #         unselected = {'marker': {'opacity': 1},'textfont': {'color': 'rgba(0,0,0,1)'}},
    #         marker={'symbol':27, 'color': 'black',  'size': 10, 'line':{'width':0}},
    #     ),dict(
    #         type='scattermapbox',
    #         mode='markers+text',
    #         lon = [9.5], lat = [32],
    #         text = 'Barra',
    #         textposition = 'middle right',
    #         hoverinfo = 'none',
    #         unselected = {'marker': {'opacity': 1},'textfont': {'color': 'rgba(0,0,0,1)'}},
    #         marker={'symbol':27, 'color': 'black',  'size': 10, 'line':{'width':0}},
    #     ),dict(
    #         type='scattermapbox',
    #         mode='markers+text',
    #         lon = [4], lat = [60+4],
    #         text = 'Number of Sightings',
    #         textposition = 'middle right',
    #         hoverinfo = 'none',
    #         textfont = {'color':'white','size':12},
    #         unselected = {'marker': {'opacity': .55},'textfont': {'color': 'rgba(255,255,255,1)'}},
    #         marker= {'size': 20,
    #                  'color':'#f47d57', 'opacity': .55,
    #                 'line': {'width': 0, 'color': 'rgba(0,0,0,0)'}},
    #     ),dict(
    #         type='scattermapbox',
    #         mode='markers+text',
    #         lon = [4], lat = [60+2],
    #         text = 'Number of Dives',
    #         textposition = 'middle right',
    #         hoverinfo = 'none',
    #         textfont = {'color':'white','size':12},
    #         unselected = {'marker': {'opacity': 1},'textfont': {'color': 'rgba(255,255,255,1)'}},
    #         marker= {'size': 20,
    #              'color':'rgba(0,0,0,0)', #nofill for this marker
    #              'line': {'width': .5, 'color': 'rgba(255,255,255,1'},
    #              'opacity': 1},
    #     ),dict(
    #         type='scattermapbox',
    #         mode='markers+text',
    #         lon = [4], lat = [60+6],
    #         selectgroup=list(range(len(xArr))),
    #         hoverinfo ='none',
    #         textposition = 'middle right',
    #         text = 'Dive Site',
    #         textfont = {'color':'white','size':12},
    #         unselected = {'marker': {'opacity': 1},'textfont': {'color': 'rgba(255,255,255,1)'}},
    #         marker={'symbol':2, 'color': locationColors,  'size': 4, 'line':{'width':0}},
    #     )]


    # layout = dict(
    #         uirevision=True,
    #         title = 'Sightings At Dive Sights',
    #         hoverlabel = { 
    #             'bordercolor': '#117a86',
    #             'bgcolor': 'white',
    #             'font': {
    #                 'family': 'Open Sans',
    #                 'size': '16',
    #                 'color': '#117a86',
    #                 }
    #             },
    #         titlefont = {
    #             'size': 16,
    #             'color': '#a8a8a8',
    #             'family': 'Open Sans'
    #             },
    #         xaxis = {'showgrid': False, 'showticklabels': False, 'visible':False},
    #         yaxis = {'showgrid': False, 'showticklabels': False, 'visible':False},
    #         showlegend=False,
    #         hovermode = 'closest',
    #         autosize = False,
    #         paper_bgcolor='rgba(0,0,0,0)',
    #         plot_bgcolor='#92d7ea',
    #         margin={'t': 40, 'b':0 , 'r':0, 'l': 0, 'pad': 1},
    #         dragmode='pan',
    #         clickmode='event+select',
    #         updatemenus = getUpdateMenus(),

    #         mapbox=dict(
    #                 uirevision=True,
    #                 accesstoken=mapboxtoken,
    #                 style='light',
    #                 bearing=0,
    #                 center=dict(lat=-23.855842, lon= 35.546857),
    #                 pitch=0,
    #                 zoom=10
    #             ),
    #        )

    # fig = dict( data=data, layout=layout )

    # return fig

