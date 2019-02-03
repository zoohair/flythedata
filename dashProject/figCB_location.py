import dash
from .server import app, Output, Input, State, dcc, html, log, mapboxtoken

import numpy as np
import datetime
import colorlover as cl

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

    selectedAirlines   = xCfgAirlines.get('airlines', dataModule.Airlines)
    selectedAircraft   = xCfgAircraft.get('aircraft', dataModule.Aircraft)

    routes = dataModule.filterData(dataModule.Airports, selectedAirlines, selectedAircraft)


    YlOrRd = cl.scales['9']['seq']['YlOrRd']
    clrscale = cl.to_rgb(cl.interp( YlOrRd, 10 ))


    geoj = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  174.74475860595703,
                  -36.86533886128865
                ],
                [
                  174.77737426757812,
                  -36.86533886128865
                ],
                [
                  174.77737426757812,
                  -36.84913134182603
                ],
                [
                  174.74475860595703,
                  -36.84913134182603
                ],
                [
                  174.74475860595703,
                  -36.86533886128865
                ]
              ]
            ]
          }
        }
      ]
    }


    layers = []
    totallines = 0
    for i, (airline, df) in enumerate(routes.groupby('airline')):
        col = clrscale[i % len(clrscale)]

        if totallines > 1000:
            break

        line_features = []
        for j , (index, row) in enumerate(df.iterrows()):
            totallines += 1
            if j > 10:
                break

            line = { "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [row['srcLonLat'], row['destLonLat']]
                    }
                    }

            line_features.append(line)

        geojsonDict = {'type': 'FeatureCollection', 
                       'features': line_features}

        layers += [dict(sourcetype = 'geojson',
                     source = geojsonDict,
                     color= col,
                     type = 'line',
                     line= {'width': 1},
                    )
                 ]  


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
                    zoom=.1,
                    layers=layers,
                ),
           )

    fig = dict( data=data, layout=layout )

    return fig

