import dash
from .server import app, Output, Input, State, dcc, html, log, mapboxtoken

import numpy as np
import datetime
import colorlover as cl

#data import
from . import dataModule


import pyproj
#TODO: use xsrc and ysrc to avoid duplicating data?

########################################
########################################
@app.callback(
    Output('WorldMapGraph', 'figure'),
    [Input('AircraftDropdown','value'), Input('xCfgAirlines', 'data')])
def genLocationFigure(xCfgAircraft, xCfgAirlines):
########################################
########################################

    selectedAirlines   = xCfgAirlines.get('airlines', dataModule.Airlines)
    selectedAircraft   = xCfgAircraft

    routes = dataModule.filterData(dataModule.Airports, selectedAirlines, selectedAircraft)


    YlOrRd = cl.scales['9']['seq']['YlOrRd']
    clrscale = cl.to_rgb(cl.interp( YlOrRd, 10 ))


    layers = []
    totallines = 0


    #For visualization, we can drop any city pairs regardless of airlines/aircraft/etc.
    
    for i, (srcCnt, df1) in enumerate(routes.groupby(['srcCountry'])):

        line_features = []
        col = clrscale[i % len(clrscale)]

        if totallines > 1000/20:
            log.warning('Reached maximum number of lines that should be drawn ...')
            break


        for destCnt, df in df1.groupby('destCountry'):

            totallines += 1


            #only consider international flights
            # if(destCnt == srcCnt) : continue 

            for x, row in df.iterrows():
                # row = dict(
                #   srcLat  = (df['srcLat']),
                #   srcLon  = (df['srcLon']),
                #   destLat = (df['destLat']),
                #   destLon = (df['destLon'])
                # )

                line = { "type": "Feature",
                         "geometry": {
                            "type": "LineString",
                            "coordinates": geoline([row['srcLon'], row['srcLat']], [row['destLon'], row['destLat']])
                            },
                        }

                line_features.append(line)

        geojsonDict = {'type': 'FeatureCollection', 
                        'features': line_features}

        layers += [dict(sourcetype = 'geojson',
           source = geojsonDict,
           color = col,
           type = 'line',
           #line= {'width': 1},
           opacity=.2
          )
        ]  






    # for i, (airline, df) in enumerate(routes.groupby('airline')):
    #     col = clrscale[i % len(clrscale)]

    #     if totallines > 2000:
    #         log.warning('Reached maximum number of lines that should be drawn ...')
    #         break

    #     line_features = []
    #     for j , (index, row) in enumerate(df.iterrows()):
    #         totallines += 1
    #         if j > 10:
    #             break

    #         line = { "type": "Feature",
    #                 "geometry": {
    #                     "type": "LineString",
    #                     "coordinates": [[row['srcLon'], row['srcLat']], [row['destLon'], row['destLat']]]
    #                 }
    #                 }

    #         line_features.append(line)

    #     geojsonDict = {'type': 'FeatureCollection', 
    #                    'features': line_features}

    #     layers += [dict(sourcetype = 'geojson',
    #                  source = geojsonDict,
    #                  color= col,
    #                  type = 'line',
    #                  line= {'width': 1},
    #                  opacity=.3
    #                 )
    #              ]  


    data = [{'type': 'scattermapbox'}]

    layout = dict(
            uirevision=True,
            title = 'World View',
            hoverlabel = { 
                'bordercolor': '#117a86',
                'bgcolor': 'white',
                'font': {
                    'family': 'Open Sans',
                    'size': '16',
                    'color': '#117a86',
                    }
                },
            titlefont = {
                'size': 16,
                'color': '#a8a8a8',
                'family': 'Open Sans'
                },
            xaxis = {'showgrid': False, 'showticklabels': False, 'visible':False},
            yaxis = {'showgrid': False, 'showticklabels': False, 'visible':False},
            showlegend=False,
            hovermode = 'closest',
            autosize = False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#92d7ea',
            margin={'t': 40, 'b':0 , 'r':0, 'l': 0, 'pad': 1},
            dragmode='pan',
            clickmode='event+select',
            # updatemenus = getUpdateMenus(),

            mapbox=dict(
                    uirevision=True,
                    accesstoken=mapboxtoken,
                    style='dark',
                    bearing=0,
                    center=dict(lat=0,lon=0),
                    pitch=0,
                    zoom=.5,
                    layers=layers,
                ),
           )

    fig = dict( data=data, layout=layout )

    return fig



def geoline(start, end):
    # calculate distance between points
    g = pyproj.Geod(ellps='WGS84')

    lonlats = g.npts(start[0], start[1], end[0], end[1], 20)

    # npts doesn't include start/end points, so prepend/append them
    lonlats.insert(0, start)
    lonlats.append(end)


    switchdir = 0
    for i, lonlat in enumerate(lonlats):
        if switchdir != 0:
            lonlats[i] = [lonlat[0] - switchdir * 360, lonlat[1]]
            continue

        if i > 0 and np.abs(lonlat[0] - lonlats[i-1][0]) > 180:
            switchdir = np.sign(lonlat[0] - lonlats[i-1][0])
            lonlats[i] = [lonlat[0] - switchdir * 360, lonlat[1]]




    return lonlats


