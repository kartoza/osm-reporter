# -*- coding:utf-8 -*-
"""Configuration options for the osm reporter app.
:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""
import os
# List of OSM pseudos
CREW = os.environ.get('CREW').split(',') \
    if os.environ.get('CREW', False) else []
# Default bbox
BBOX = os.environ.get('BBOX') \
    if os.environ.get('BBOX', False) else \
    '20.411482,-34.053726,20.467358,-34.009483'
# Whether to display the "update stats control" on the map
# Set to 0 or 1 if using an env var
DISPLAY_UPDATE_CONTROL = os.environ.get('DISPLAY_UPDATE_CONTROL') \
    if os.environ.get('DISPLAY_UPDATE_CONTROL', False) else True

# Where to store OSM files
CACHE_DIR = os.environ.get('CACHE_DIR') \
    if os.environ.get('CACHE_DIR', False) else '/tmp'
# Where to store bbox json logs - one for each data request
# On docker/rancher we will pass this var in
# for other systems we default to /tmp
LOG_DIR = os.environ.get('LOG_DIR') \
    if os.environ.get('LOG_DIR', False) else '/tmp'
# Options for the osm2pgsql command line
OSM2PGSQL_OPTIONS = os.environ.get('OSM2PGSQL_OPTIONS') \
    if os.environ.get('OSM2PGSQL_OPTIONS', False) else ''
