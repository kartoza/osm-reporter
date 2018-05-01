import os
from reporter import config


class Pathor:
    """
    Pathor Object
    Each frame has a Pathor object to store path of the frame's files:
    - ways.txt
    - image.png
    - frame.png
    - label.png
    - encoded_frame/
    """
    def __init__(self, frame_id):
        """
        Constructor
        :param frame_id: the id of a frame (e.g: 2010-01)
        :type frame_id: string
        """
        self.frame_id = frame_id
        self.path = '{}{}/'.format(config.TMP_PATH, frame_id)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.ways = '{}ways.txt'.format(self.path)
        self.image = '{}image.png'.format(self.path)
        self.frame = '{}frame.png'.format(self.path)
        self.label = '{}label.png'.format(self.path)
        self.encoded_frame = '{}encoded_frame'.format(self.path)
