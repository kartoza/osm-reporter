import os
from reporter import config
from reporter.animate.osm_data import OsmData
from reporter.animate.frame import (
    Frame,
    build_init_frame,
    build_gif
)
# from reporter.utilities import LOGGER


class OsmGif:
    """
    OsmGif transforms an OSM file into a GIF file
    """

    def __init__(self, osm_file):
        """
        Constructor

        :param osm_file: the path of an OSM file
        :type osm_file: string

        :returns: an instance of OsmGif
        :rtype: OsmGif
        """
        self.osm_file = osm_file
        self.filename = os.path.splitext(os.path.basename(self.osm_file))[0]
        self.gif_file = '{}{}.gif'.format(config.GIF_PATH, self.filename)

    def run(self):
        """
        Where the magic happens.
        """

        # if the gif already exists, we return immediately
        if os.path.isfile(self.gif_file):
            return

        # get an OsmData object
        osm_data = OsmData(self.osm_file)

        # build each frame
        for frame_id in osm_data.frames():
            Frame(frame_id).build(osm_data)

        # build the init frame
        build_init_frame()

        # build the final gif
        build_gif(self.gif_file)


def osm_to_gif(osm_file):
    """
    Animate an OSM file: create an object OsmGif and run

    :param osm_file: path of an OSM file
    :type osm_file: string

    :returns: path of the gif file
    :rtype: string
    """
    osm_gif = OsmGif(osm_file)
    osm_gif.run()
    return osm_gif.gif_file
