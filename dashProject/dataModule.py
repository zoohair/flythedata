import pandas as pd
import os
import numpy as np
import datetime


################################################
################################################
################################################


import logging
logging.basicConfig(format='%(levelname)s|%(name)s|\t %(message)s',level=logging.INFO)
log = logging.getLogger('dataModule')


################################################
################################################
################################################

def loadData(dataFolder):
    #Load the data
    routesFile   = os.path.join(dataFolder,'routes.dat')
    airportsFile = os.path.join(dataFolder,'airports-extended.dat')
    airlinesFile = os.path.join(dataFolder,'airlines.dat')
    routes   = pd.read_csv(routesFile)
    airports = pd.read_csv(airportsFile)
    airlines = pd.read_csv(airlinesFile)

    #Get airline names and add column
    airlineIDs = {}
    for ID in routes['airlineID'].unique():
        #IDs in the airlines File are integers
        try:
            IDint = int(ID)
        except:
            IDint = -1
        airlineIDs[ID] = airlines[airlines['airlineID'] == int(IDint)]['name'].values[0]
    getAirlineName = lambda row: airlineIDs[row['airlineID']]

    routes['airline'] = routes.apply(getAirlineName, axis=1)

    #Get airport data and add to dataframe
    airportIDs = {}
    for ID in np.unique(np.concatenate([routes['srcAirportID'].unique() , routes['destAirportID'].unique()])):
        try:
            #IDs in the airport File are integers
            IDint = int(ID)
            thisairport = airports[airports['airportID'] == IDint]
            
            #get name and strip "Airport" from the end
            airportName = thisairport['name'].values[0]
            airportName = airportName.split(' ')
            if airportName[-1] == 'Airport': airportName.pop()
                
            #save data including lat/lon
            airportIDs[ID] = {'name': ' '.join(airportName), 
                              'lonlat': [thisairport['lon'].values[0], thisairport['lat'].values[0]]}
            
        except:
            log.debug('airport ID %s not found in database'%ID)
            airportIDs[ID] = {'name': '???', 'lonlat': [0,0]}
    airportLookup = lambda ID, attr: airportIDs[ID][attr]


    routes['srcAirport']  = routes['srcAirportID'].apply(airportLookup,args=['name'])
    routes['destAirport'] = routes['destAirportID'].apply(airportLookup,args=['name'])


    routes['srcLonLat'] = routes['srcAirportID'].apply(airportLookup, args=['lonlat'])
    routes['destLonLat'] = routes['destAirportID'].apply(airportLookup,args=['lonlat'])


    #drop any route where src/dest airports are not known
    droprows =  routes.loc[np.logical_or(routes['destAirport'] == '???' , routes['srcAirport'] == '???')]
    routes.drop(droprows.index, inplace=True)
        
    #drop any route that is codeshare or has stops
    droprows =  routes.loc[np.logical_or(~routes['codeshare'].isna() , routes['stops'] > 0)]
    routes.drop(droprows.index, inplace=True)


    #Split the aircraft field into an array of strings
    routes.drop(routes.loc[routes['aircraft'].isna()].index, inplace=True)
    routes['aircraft'] = routes['aircraft'].astype(str)
    routes['aircraft'] = routes['aircraft'].apply(lambda s: s.split(' '))



    #drop "return" flights. OK for now until we want to do capacity analysis (i.e. direction of flight matters!) 
    srcDestKey = lambda row: '-'.join(np.sort([row['srcAirportIATA'] , row['destAirportIATA']]))
    routes['srcDestSorted'] = routes.apply(srcDestKey,axis=1)
    routes.drop_duplicates(subset=['airline', 'srcDestSorted'],inplace=True)

    #drop unused columns
    routes.drop(['airlineIATA', 'airlineID', 'srcAirportIATA', 'destAirportIATA',
                 'srcAirportID', 'destAirportID', 'codeshare', 'stops'], axis='columns',inplace=True)


    return routes


log.info('Loading routes data!')
routesData = loadData(os.path.join(os.path.dirname(__file__), './dataFolder'))


Airports = routesData['srcAirport'].unique()
Airlines = routesData['airline'].unique()
Aircraft = np.unique(np.concatenate(routesData['aircraft'].values))

def filterData(selectedAirports, selectedAirlines, selectedAircraft):


    log.warn('Need to implement filterData function. For now no filtering is implemented!')

    return routesData



