import subprocess
import re
import os

from reporter import config
from reporter.animate.pathor import Pathor
from reporter.utilities import LOGGER

class Frame:

    """
    Frame is an object representing a frame of the final GIF
    A frame has an ID (a date).
    A frame gathers all ways that have the same date.
    """
    def __init__(self, frame_id):
        """
        Constructor

        :param frame_id: the id of the frame with the format:
            YYYY-MM (e.g: 2010-01)
        :type frame_id: string
        """
        self.frame_id = frame_id
        self.paths = Pathor(self.frame_id)

    def build(self, osm_data):
        """
        Build a frame.png (image.png + label.png) from a frame_id:
        - Fetch the coordinates that belongs to the frame
        - encode and render the image
        - render the label
        - render the frame

        :param osm_data: Data that every frame must access: ways and bounds
        :type osm_data: OsmData instance

        """
        self.osm_data = osm_data
        coordinates = self.osm_data.filter_coordinates_for_frame(self.frame_id)
        
        with open(self.paths.ways, 'w') as frame:
            frame.write(''.join(coordinates))

        self.encode_image()
        self.render_image()
        self.render_label()
        self.render_frame()

    def width(self):
        """
        Run the command `identify` on the image.png

        :returns: the width of the image.png
        :rtype: string
        """
        image_output = subprocess.check_output(['identify', self.paths.image])
        return re.search('PNG (\\d+)x\\d+', str(image_output)).group(1)

    def height(self):
        """
        Run the command `identify` on the image.png

        :returns: the height of the image.png
        :rtype: string
        """
        image_output = subprocess.check_output(['identify', self.paths.image])
        return re.search('PNG \\d+x(\\d+)', str(image_output)).group(1)

    def encode_image(self):
        """
        Encode coordinates

        :returns: None
        """
        if os.path.exists(self.paths.ways):
            command = 'cat {} | {}encode -o {} -z {}'.format(
                self.paths.ways,
                config.BIN_PATH,
                self.paths.encoded_frame,
                config.ZOOM_LEVEL)

        os.system(command)

    def render_image(self):
        """
        Render an image with the encoded frame and the boundaries

        :returns: None
        """
        if (os.path.exists(self.paths.encoded_frame)
                and self.osm_data.bounds != None):
            command1 = '{}render -t 0 -A -- "{}" {}'.format(
                config.BIN_PATH,
                self.paths.encoded_frame,
                config.ZOOM_LEVEL)

            command2 = '{} {} {} {}'.format(
                self.osm_data.bounds['minlat'],
                self.osm_data.bounds['minlon'],
                self.osm_data.bounds['maxlat'],
                self.osm_data.bounds['maxlon'])

            command3 = '> {}'.format(self.paths.image)

            os.system('{} {} {}'.format(command1, command2, command3))

    def render_label(self):
        """
        Create a .png file of the label

        :returns: None
        """
        command1 = 'convert -size {}x50 -gravity Center' \
            ' -background black'.format(self.width())
        command2 = '-stroke white -fill white label:\'{}\' {}'.format(
            self.frame_id, self.paths.label)

        os.system('{} {}'.format(command1, command2))

    def render_frame(self):
        """
        Render a frame using the image and the label

        :returns: None
        """
        command = 'convert -append {} {} {}'.format(
            self.paths.image,
            self.paths.label,
            self.paths.frame)

        os.system(command)


def build_init_frame():
    """ Build the init frame.
    We need to build the first frame before building the init frame.
    The init frame is an image with black background.
    It has the same height/width as the first frame
    """

    # get the first frame directory
    first_frame_id = os.listdir(config.TMP_PATH)[0]
    # create a instance of this Frame
    first_frame = Frame(first_frame_id)

    # create the directory for the init frame: 0000-00
    init_frame_dir = '{}/0000-00'.format(config.TMP_PATH)
    os.makedirs(init_frame_dir)

    frame = '{}/frame.png'.format(init_frame_dir)

    # create the 0000-00/frame.png
    command = 'convert -size {}x{} canvas:black {}'.format(
        first_frame.width(),
        str(int(first_frame.height()) + 50),
        frame)

    os.system(command)

def build_gif(gif_file):
    """ Build the final Gif

    :param gif_file: the path of the final GIF
    :type gif_file: string

    :returns: None
    """
    frames = '{}*/frame.png'.format(config.TMP_PATH)

    command = 'convert -coalesce -dispose 1 -delay 20 -loop 0 {} {}'.format(
        frames, gif_file)
    os.system(command)

    command = 'convert {} \\( +clone -set delay 500 \\)' \
        ' +swap +delete {}'.format(gif_file, gif_file)
    os.system(command)
