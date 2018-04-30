import os
from reporter.test.logged_unittest import LoggedTestCase
from reporter.test.helpers import (
    SWELLENDAM_OSMFILE_PATH
)
# from reporter.utilities import LOGGER
from reporter import config

from reporter.animate.frame import (
    Frame,
    build_init_frame,
    build_gif
)

from reporter.animate.osm_data import OsmData
from reporter.animate.util import (
    mkdir_tmp
)

class FrameTestCase(LoggedTestCase):
    def setUp(self):
        mkdir_tmp()

    def test_build_one_frame(self):
        """
        it should build one frame:
        """
        frame_id = '2010-01'
        osm_data = OsmData(SWELLENDAM_OSMFILE_PATH)
        working_dir = '{}{}'.format(config.TMP_PATH, frame_id)

        frame = Frame(frame_id)
        frame.build(osm_data)
        # - create a working directory for the frame
        self.assertTrue(os.path.exists(working_dir))

        # - write coordinates in dir/ways.txt
        self.assertTrue(os.path.exists('{}/ways.txt'.format(working_dir)))

        # - create a working directory for the encoded frame
        self.assertTrue(os.path.exists('{}/encoded_frame/'.format(working_dir)))

        # - render the image
        self.assertTrue(os.path.exists('{}/image.png'.format(working_dir)))

        # - render the label
        self.assertTrue(os.path.exists('{}/label.png'.format(working_dir)))

        # - render the frame
        self.assertTrue(os.path.exists('{}/frame.png'.format(working_dir)))

    def test_build_first_frame(self):
        """
        it should build the frame 0000-00
        """

        # first we build the first frame
        frame_id = '2010-01'
        osm_data = OsmData(SWELLENDAM_OSMFILE_PATH)
        frame = Frame(frame_id)
        frame.build(osm_data)

        init_frame_dir = '{}/0000-00'.format(config.TMP_PATH)
        init_frame = '{}/frame.png'.format(init_frame_dir)

        # then we build the init frame
        build_init_frame()

        self.assertTrue(os.path.exists(init_frame_dir))
        self.assertTrue(os.path.exists(init_frame))

    def test_build_gif(self):
        """
        it should build a gif of two frames (init + first_frame)
        """

        frame_id = '2010-01'
        osm_data = OsmData(SWELLENDAM_OSMFILE_PATH)
        frame = Frame(frame_id)
        frame.build(osm_data)
        build_init_frame()

        gif_file = '{}{}.gif'.format(config.GIF_PATH, 'my_gif')

        build_gif(gif_file)

        self.assertTrue(os.path.exists(gif_file))
