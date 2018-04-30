import re
import os
from bs4 import BeautifulSoup
from reporter.animate.util import (
    format_timestamp,
    mkdir_tmp
)
#from reporter.utilities import LOGGER
from reporter import config

class OsmData:
    """ OsmData object to store data from the OSM file:
    - <way> tags
    - <bounds> tag
    - datamap file content (from the snap command)
    Those data will be used by every Frame to be built.
    """
    def __init__(self, osm_file):
        """ Constructor

        :param osm_file: The path of the OSM file
        :type osm_file: str

        :returns: A OsmData instance
        :rtype: OsmData
        """
        try:
            soup = BeautifulSoup(open(osm_file), 'html.parser')
        except FileNotFoundError:
            self.ways = None
            self.bounds = None
            self.datamap = None
        else:
            self.ways = soup.find_all('way')
            self.bounds = soup.find('bounds')
            self.datamap = snap_datamap(osm_file)

    def frames(self):
        """
        Create an array of unique date (YYYY-MM)

        :returns: A sorted set/map of unique date (frame)
        :rtype: set
        """
        return sorted(set(map(
            lambda way: 
            format_timestamp(way['timestamp']), self.ways
        )))

    def filter_coordinates_for_frame(self, frame):
        """
        Find coordinates that belongs to a frame

        :param frame: the id of the frame (e.g: '2010-01')
        :type frame: str

        :returns: A list of coordinates
        :rtype: list
        """
        ways = self.map_ways_for_frame(frame)
        return list(filter(
            lambda line:
            re.search("id=(\\d+)", line).group(1) in ways, self.datamap
        ))

    def map_ways_for_frame(self, frame):
        """
        Map a list containing only the id of the Way objects

        :param frame: the id of the frame (e.g: '2010-01')
        :type frame: str

        :returns: A list of way id (str)
        :rtype: list
        """
        return list(map(
            lambda way: way['id'], self._filter_ways_for_frame(frame)
        ))

    def _filter_ways_for_frame(self, frame):
        """
        Filter Way objects that belongs to a frame

        :param frame: the id of the frame (e.g: '2010-01')
        :type frame: str

        :returns: A list of Way objects
        :rtype: list
        """
        return list(filter(
            lambda way:
            frame == format_timestamp(way['timestamp']), self.ways
        ))

def snap_datamap(osm_file):
    mkdir_tmp()
    if os.path.exists(osm_file):
        command = 'cat {} | {}snap > {}'.format(
            osm_file,
            config.BIN_PATH,
            config.DATAMAP)

        os.system(command)
    try:
        with open(config.DATAMAP, 'r') as datamapfile:
            return datamapfile.readlines()
    except FileNotFoundError:
        return None
