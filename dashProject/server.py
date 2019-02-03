####################################
###     Module Importing         ###
####################################

#Import Dash and plotly modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
import plotly.graph_objs as go

#Importing the safe dump/load functions of yamls
#see https://security.openstack.org/guidelines/dg_avoid-dangerous-input-parsing-libraries.html
from yaml import safe_dump as yamlSDump, safe_load as yamlSLoad
import textwrap



#Using Flask Session to keep track of global data
from flask import Flask

##
import os
projDIR = os.path.dirname(__file__)


import logging
logging.basicConfig(format='%(levelname)s|%(name)s|%(asctime)s|\t %(message)s',level=logging.INFO)
log = logging.getLogger('dashApp')

from . import htmlHelpers


####################################
### Configuring Dash application ###
####################################

#Whether to run dash offline and with debugging!
#We rely on 'DYNO' variable being present on heroku to
#turn off the debugging!
debugApp = not('DYNO' in os.environ)

if 'MAPBOX_TOKEN' in os.environ:
    mapboxtoken = os.environ['MAPBOX_TOKEN']
else:
    log.warning('No MAPBOX_TOKEN defined in the environment!')
    mapboxtoken = 'NOTOKEN'

#When debugging, also assume wewill be serving files locally
offlineApp = debugApp


server = Flask(__name__)
app = dash.Dash("FlyTheData", server=server, meta_tags = 
                [{'name':"viewport", 'content':"width=device-width, initial-scale=1"}])

app.index_string = htmlHelpers.generateIndexString()


app.server.config.from_object(__name__)
app.server.secret_key = 'theansweris42'.encode('utf8') #should'nt matter since we're doing server side storage


portnumber=4000
#Allowing offline:
app.css.config.serve_locally = offlineApp
app.scripts.config.serve_locally = offlineApp 

plotlyConfig = {'displayModeBar': 'hover', 'responsive': True,
                'scrollZoom': False,
                'modeBarButtonsToRemove': [ 'sendDataToCloud', 'lasso2d', 'zoomIn2d', 'zoomOut2d', #'toImage',
                    'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines', 'toggleHover'],
                'displaylogo': False }
if not offlineApp: #i.e. running online
    #Load any css/scripts/etc. from the wild WWW
    pass
else:
    log.warning('Running offline, If using maps, make sure topojson files properly in assets folder')
    plotlyConfig['topojsonURL'] = 'http://127.0.0.1:%i/assets/'%portnumber

if debugApp: log.setLevel(logging.DEBUG)


# @server.route("/update")
# def updatePage():
#     return '''
#     <p>
#     This page will eventually run a script which will update
#     the sightings database by pulling from a google spreadsheet(s)
#     and updating the .csv files
#     </p> 
#     '''

