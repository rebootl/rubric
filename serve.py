#!/usr/bin/python
'''simple webserver for new_simple_cms

Using the python module http.server.

CGI enabled.
'''

# Import 
# python modules
import os
from http.server import HTTPServer, CGIHTTPRequestHandler

PUBLIC_DIR = "/home/cem/website_rubric/public/"

## Change WD:
os.chdir(PUBLIC_DIR)

## Server:
serve=HTTPServer(('', 8001), CGIHTTPRequestHandler)
serve.serve_forever()
