import dash
from .server import app, Output, Input, State, dcc, html, log

#data import
from . import dataModule
from .diveSiteLocations import diveSiteLoc

import numpy as np

########################################
########################################
@app.callback(
    Output('species', 'figure'),
    [Input('xCfgDates', 'data'), Input('xCfgLocations', 'data')],
    [State('xCfgSpecies', 'data')])
def genSpeciesFigure(xCfgDates, xCfgLocations, xCfgSpecies):
########################################
########################################
    if xCfgDates == {} or xCfgLocations == {}:
        log.debug('Not ready to render Species Figure')
        raise dash.exceptions.PreventUpdate()

    log.debug('Rendering Species Figure')

    date_start, date_end = xCfgDates.get('dateRange', dataModule.dateRange)
    selectedDiveSites = xCfgLocations.get('diveSites', dataModule.diveSites)

    speciesList = dataModule.speciesList

    selectedSpecies = xCfgSpecies.get('species', speciesList)

    filteredData, _ = dataModule.filterData(date_start, date_end, 
                        speciesList, selectedDiveSites, 
                        'Site')


    nSeen = [filteredData[s].sum() for s in speciesList]
    text = ['%s: %i Sightings'%(s,n) for (s,n) in zip(speciesList, nSeen) ]
    colors = [dataModule.colorLookup(s) for s in speciesList]
 

    data = []
    for (i, s, n, t, c) in zip(range(len(nSeen)), speciesList, nSeen, text, colors):
        if not (s in speciesList):
            c = 'rgba(0,0,0,0)'
            hoverinfo = 'none'
        else:
            hoverinfo = 'text'
        data += [dict(
            type = 'bar', #bar or barpolar
            x = [i],  y = [n],
            width=.9,
            name = s,
            text = [t],
            marker = {'color': c},
            hoverinfo=hoverinfo,
            orientation='v',
            customdata=[s],
            selectedpoints=[0] if s in selectedSpecies else [],
            )]


        layout = dict(
            uirevision=True,
            title = 'Species Frequency',
            titlefont = {
                'size': 16,
                'color': '#a8a8a8',
                'family': 'Open Sans'
                },            
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,.2)',
                showticklabels=True,
                ticks='',
                tickfont={'color':'white'},
                # dtick=1,#np.log10(50),
                type='log',
                visibile=True,
                title='Number of Individuals (Log)',
                titlefont={'color':'#a8a8a8'}
                ),
            font = {'color': '#fff',},
            xaxis  = {'range': [-.5,len(nSeen)-.5], 'visible':False},
            showlegend = False,
            legend={'orientation':'v'},
            hovermode = 'closest',
            autosize = False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin={'t': 40, 'b':20 , 'r':0, 'l': 50, 'pad': 1},
            dragmode='select',
            clickmode='event+select',

            updatemenus = getUpdateMenus(),
           )

    fig = dict( data=data, layout=layout )

    return fig
    



#First, let's group the species into clades and get the indices

#This assumes that dataModule.speciesList is in the same
#order as dataModule.speciesInfo['commonName'] (modulo species that are not in the data)
#So double checking that assumption ...

speciesListInfo = dataModule.speciesInfo.loc[[s in dataModule.speciesList for s in dataModule.speciesInfo.commonName]]
speciesListInfo.reset_index(drop=True, inplace=True)
assert(np.all(speciesListInfo.commonName == dataModule.speciesList))

speciesGroups = {}
for index, species in speciesListInfo.iterrows():
    commonName = species['commonName']
    group = species['clade']
    if group in speciesGroups:
        speciesGroups[group].append(index)
    else:
        speciesGroups[group] = [index]


#Next, let's create the  updateMenues to be used
global updateMenus
updateMenus = [
    dict(type="dropdown", 
         font = {'size': 12, 'color': '#404545'},
         bgcolor = '#f1f2f2', bordercolor= 'white', borderwidth= 1,
         direction = 'down', xanchor = 'right', x=1, yanchor = 'top', y=1,
         pad={'t': 5, 'b':5 , 'r':5, 'l': 0},
         active=0, showactive = False,
         buttons=[]
        ),
    ]
traceIndices = range(len(dataModule.speciesList))



button = {
    'method': 'skip',
    'args': [],
    'label' : 'Select Species', #label the button with the group name
}
updateMenus[0]['buttons'].append(button)

button = {
    'method': 'update',
    'args': [{'SelectFromUpdateMenu': True, #signal to callback this is a selection
              'selectedpoints': [[0]*len(traceIndices)] #list of indices for this group
             },
             #layout will default to {}
             #traces will default to all traces
            ],
    'label' : 'All Species', #label the button with the group name
}
updateMenus[0]['buttons'].append(button)


for group, indices in speciesGroups.items():
    selectedpoints = [[0] if i in indices else [] for i in traceIndices] 
    button = {
        'method': 'update',
        'args': [{'SelectFromUpdateMenu': True, #signal to callback this is a selection
                  'selectedpoints': selectedpoints #list of indices for this group
                 },
                 #layout will default to {}
                 #traces will default to all traces
                ],
        'label' : group, #label the button with the group name
    }
    updateMenus[0]['buttons'].append(button)


def getUpdateMenus():
    global updateMenus
    return updateMenus