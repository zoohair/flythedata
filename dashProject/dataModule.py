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


log.info('Loading routes info!')

def loadData(filename):

    df = pd.read_csv(filename)

    #need to read airport data as well ...

    log.warn('Need to clean up data')

    return df


log.info('Loading routes data!')
routesData = loadData(os.path.join(os.path.dirname(__file__), './dataFolder/routes.dat'))


log.warn('Need to properly do this')
Airports = routesData['destAirport'].unique()
Airlines = routesData['airlineIATA'].unique()
Aircraft = routesData['aircraft'].unique()

def filterData(selectedAirports, selectedAirlines, selectedAircraft):

    global routesData

    log.warn('Need to implement filterData function')

    return routesData



