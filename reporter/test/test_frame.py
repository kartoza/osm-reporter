import os
from reporter.test.logged_unittest import LoggedTestCase
from reporter.test.helpers import (
    SWELLENDAM_OSMFILE_PATH,
    BIG_IMAGE,
    TMP_BIG_IMAGE,
    SMALL_IMAGE,
    TMP_SMALL_IMAGE
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

    def test_resize_image_when_big(self):
        """
        it should resize a big image to 940x350
        """
        # new fake frame
        frame = Frame('frame_id')

        # use a copy of a big image
        command = 'cp {} {}'.format(BIG_IMAGE, TMP_BIG_IMAGE)
        os.system(command)

        # change frame's image's path
        frame.paths.image = TMP_BIG_IMAGE

        # it should be a big image
        self.assertEqual(frame.width(), '3760')

        frame.resize_image()

        # it should be resized to 940
        self.assertEqual(frame.width(), '940')

        # remove the resized image
        command = 'rm {}'.format(TMP_BIG_IMAGE)
        os.system(command)

    def test_resize_image_when_small(self):
        """
        it should resize a small image to 940x350
        """

        # new fake frame
        frame = Frame('frame_id')

        # use a copy of a small image
        command = 'cp {} {}'.format(SMALL_IMAGE, TMP_SMALL_IMAGE)
        os.system(command)

        frame.paths.image = TMP_SMALL_IMAGE

        self.assertEqual(frame.width(), '469')

        frame.resize_image()

        # 938, 940, same, same
        self.assertEqual(frame.width(), '938')

        # remove the resized image
        command = 'rm {}'.format(TMP_SMALL_IMAGE)
        os.system(command)

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
        self.assertTrue(
            os.path.exists('{}/encoded_frame/'.format(working_dir)))

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
