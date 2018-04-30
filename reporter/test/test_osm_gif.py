import os
from reporter.test.logged_unittest import LoggedTestCase
from reporter.test.helpers import (
    SWELLENDAM_OSMFILE_PATH
)

from reporter.animate.osm_gif import (
    OsmGif,
    osm_to_gif
)

# from reporter.utilities import LOGGER
from reporter import config

class OsmGifTestCase(LoggedTestCase):
    def test_init(self):
        """
        check that the osm filename is correct
        check that the gif file is correct
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        osm_gif = OsmGif(osm_file)
        self.assertEqual(osm_gif.filename, 'swellendam_with_bounds')

        gif_path = '{}swellendam_with_bounds.gif'.format(config.GIF_PATH)
        self.assertEqual(osm_gif.gif_file, gif_path)

    def test_run(self):
        """
        check that it creates a gif file
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        osm_gif = OsmGif(osm_file)
        gif_path = '{}swellendam_with_bounds.gif'.format(config.GIF_PATH)

        if os.path.isfile(gif_path):
            os.remove(gif_path)

        osm_gif.run()

        self.assertTrue(os.path.isfile(gif_path))

    def test_osm_to_gif(self):
        """
        check that it creates a gif file
        """
        gif_path = '{}swellendam_with_bounds.gif'.format(config.GIF_PATH)
        if os.path.isfile(gif_path):
            os.remove(gif_path)

        gif_file = osm_to_gif(SWELLENDAM_OSMFILE_PATH)
        self.assertEqual(gif_file, gif_path)
