import dash
from .server import app, Output, Input, State, dcc, html, log
import datetime

#data import
from . import dataModule
from .diveSiteLocations import diveSiteLoc
from .dataModule import colorLookup

import numpy as np
import copy


def dataNormalize(xIn):
    x  = np.array(xIn)

    #If this was a normal dist

    # std = np.nanstd(x)

    # if std > 0:
    #     #x = x / std + np.mean(x) * (1 - 1 / std)
    #     mu = np.mean(x)
    #     x  = x / std #(x - mu) / std + mu

    #Assume a half-normal distribution
    #Estimate sigma:
    n = len(x)
    sigma = np.sqrt(np.sum(x**2)/n)
    if sigma > 0:
        x = x / sigma

    return x

########################################
########################################
@app.callback(
    Output('longTerm', 'figure'),
    [Input('xCfgSpecies', 'data'), Input('xCfgLocations', 'data')],
    [State('xCfgDates', 'data')])
def genTimeFigure(xCfgSpecies, xCfgLocations, xCfgDates):
########################################
########################################
    if xCfgLocations == {} or xCfgSpecies == {}:
        log.debug('Not ready to render Timeline Figure')
        raise dash.exceptions.PreventUpdate()

    log.debug('Rendering Timeline Figure')

    #For plotting, get the range or use the default
    plotRange = xCfgDates.get('dateRange', dataModule.defaultDateRangeToPlot)

    #Here, we use the entire range as we need to be able to show the timeslider
    #as well as the fact that the normalization makes sense over the entire
    #data set!
    date_start , date_end = dataModule.dateRange
    selectedSpecies      = xCfgSpecies.get('species', dataModule.speciesList)
    selectedDiveSites    = xCfgLocations.get('diveSites', dataModule.diveSites)
    

    filteredData_allDates, stackSpecies = dataModule.filterData(date_start, date_end, 
                                list((selectedSpecies)), 
                                selectedDiveSites, 
                                'Species')

    dateGranularity = 'Monthly'

    if dateGranularity == 'Monthly':
        first_of_func = dataModule.first_day_of_month
        last_of_func  = dataModule.last_day_of_month
    elif dateGranularity == 'Weekly':
        first_of_func = dataModule.first_day_of_week
        last_of_func  = dataModule.last_day_of_week
    elif dateGranularity == 'Quarterly':
        first_of_func = dataModule.first_day_of_quarter
        last_of_func  = dataModule.last_day_of_quarter 


    data = []
    for subRangeIdx , (date_start, date_end) in enumerate(dataModule.dateSubRanges):
        fltr = filteredData_allDates.date.between(date_start,date_end)
        filteredData = filteredData_allDates[fltr]

        #Get firsts of month/week (make sure they are sorted)
        uniqueDates = filteredData['date'].apply(first_of_func).unique()
        uniqueDates = np.sort(uniqueDates)

        nSightsLines = {s:[] for s in stackSpecies}
        sightsLbl    = {s:[] for s in stackSpecies}

        nDivesLine= []
        nDivesLbl = []

        midDays = [] 
        for day in uniqueDates:
            lastday = last_of_func(day)
            midDays += [day + (lastday-day)/2]
            withinDateRange = filteredData['date'].between(day, lastday)
            subfilteredData = filteredData[withinDateRange]
            nDives  = subfilteredData.index.size
            nDivesLine += [nDives]
            nDivesLbl += ['{d} dives<br>during {s}'.format(d=nDives, s=day.strftime('%b-%Y'))]


            for spec in stackSpecies:
                #count number of dives
                if spec in subfilteredData:
                    nSights = subfilteredData[spec].sum()
                else:
                    nSights = 0

                nSightsLines[spec] += [nSights]

                #Create the label
                if nSights == 0:
                    txt = None #No labels if no sightings!
                else:
                    txt = '{species}:<br>{n:.0f} sightings<br>during {s}'.format(
                        species=spec, n=nSights, # d=nDives, 
                        s=day.strftime('%b-%Y'))

                sightsLbl[spec] += [txt]

        #Normalize the sightings over this time period:

        yStacked = None
        for spec in stackSpecies:
            nSightsLines[spec] = dataNormalize(nSightsLines[spec])
            #Summing up all y values to later normalize the dives lines
            if isinstance(yStacked, type(None)):
                yStacked = copy.copy(nSightsLines[spec])
            else:
                yStacked += nSightsLines[spec]

        if len(yStacked) > 0:
            yMax = np.max(yStacked)
            nDivesLine = nDivesLine / np.max(nDivesLine) * 1.2 * yMax

        for spec in stackSpecies:
            data += [dict(type='scatter',
                x = midDays, y = nSightsLines[spec], yaxis='y',
                hoverinfo = 'text',text = sightsLbl[spec],
                mode = 'lines',
                line = {'color': colorLookup(spec),
                        'shape':'spline',
                        'width': 0, 'opacity': 1
                        },
                marker={'opacity': 1},
                showlegend=False,
                stackgroup=str(date_start),
                fillcolor = colorLookup(spec),
                )]

        data += [dict(type='scatter',
                    x = midDays,  y = nDivesLine, yaxis='y',
                    hoverinfo = 'text', text = nDivesLbl,
                    mode = 'lines',
                    name = '# of Dives',
                    legendgroup = 'diveEffort',
                    showlegend = subRangeIdx == 0,
                    line = {'shape':'spline', 
                            'color': 'white', 'width': 2, 'opacity': 0},
                    )]
    

    layout = dict(
            uirevision=True,
            title = 'Sightings Over Time',
            titlefont = {
                'size': 16,
                'color': '#a8a8a8',
                'family': 'Open Sans'
                },
            showlegend=True,
            legend={'x': 0, 'y':1, 'font':{'color':'white'}},
            hovermode = 'closest',
            autosize = False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            color="#fff",
            margin={'t': 60, 'b':0 , 'r':0, 'l': 40},
            dragmode='pan',
            #updatemenus=updateMenus,
            yaxis=dict(title='Sightings',
                type='linear', side='left',
                showgrid=True, 
                gridcolor='#a8a8a8',
                showticklabels=False,
                #tickvals = [-4, -2, 0, 2, 4],
                #ticktext = ['-4\u03c3', '-2\u03c3', '0', '2\u03c3', '4\u03c3'],
                tickfont={'color':'white'},
                titlefont={'color':'#a8a8a8'},
                #range=[-4,4],
                ),
            # yaxis2=dict(
            #     type='linear', side='right',
            #     showgrid=False, 
            #     gridcolor='#a8a8a8',
            #     showticklabels=False,
            #     #tickvals = [-4, -2, 0, 2, 4],
            #     #ticktext = ['-4\u03c3', '-2\u03c3', '0', '2\u03c3', '4\u03c3'],
            #     tickfont={'color':'white'},
            #     titlefont={'color':'#a8a8a8'},
            #     #range=[-4,4],
            #     ),
            xaxis=dict(
                showgrid= True, 
                gridcolor='#a8a8a8',
                showticklabels= True, 
                tickfont={'color':'white'},
                ticks='outside',
                tickcolor='#fff',
                range= plotRange,
                rangeselector=rangeselector,
                rangeslider=dict(visible = True, thickness=.1),
                type='date'
                )
           )


    fig = dict( data=data, layout=layout )

    return fig

global rangeselector
rangeselector = dict(
                 font = {'size': 12, 'color': '#404545'},
                 bgcolor = 'white', bordercolor= 'white', borderwidth= 1,
                 direction = 'down', xanchor = 'right', x=1, yanchor = 'bottom', y=1,
                 pad={'t': 0, 'b':0 , 'r':0, 'l': 0},
                 buttons=[
                    dict(count=3, label='3 Months', step='month', stepmode='backward'),
                    dict(count=6, label='6 Months', step='month', stepmode='backward'),
                    dict(count=1, label='1 Year', step='year', stepmode='backward'),
                    dict(step='all', label='All Time')
                    ],
                 selected=2, #Doesn't seem to work on python...
                )

#Trying to rebuild the rangeselector as an updatemenu for consistancy
global updateMenus
updateMenus = [
    dict(type="dropdown", 
         font = {'size': 12, 'color': '#404545'},
         bgcolor = '#f1f2f2', bordercolor= '#404545', borderwidth= 1,
         direction = 'down', xanchor = 'right', x=1, yanchor = 'bottom', y=1,
         pad={'t': 0, 'b':0 , 'r':0, 'l': 0},
         active=0, showactive = True,
         buttons=[
                    dict(count=1, label='3 Months', step='month', stepmode='backward'),
                    dict(count=6, label='6 Months', step='month', stepmode='backward'),
                    dict(count=1, label='1 Year', step='year', stepmode='backward'),
                    dict(step='all', label='All Time')
                    ]
        ),
    ]