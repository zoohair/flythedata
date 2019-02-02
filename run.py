#!/usr/bin/env python3

from dashProject.app import app
import dashProject.server as server

if __name__ == '__main__':
    app.run_server(debug=server.debugApp, port=server.portnumber)#, host= '0.0.0.0') 
