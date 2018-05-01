from reporter.test.logged_unittest import LoggedTestCase
# from reporter.utilities import LOGGER
from reporter import config
from reporter.animate.pathor import Pathor


class PathorTestCase(LoggedTestCase):
    def test_init(self):
        frame_id = 'pathor-test'
        working_dir = '{}{}/'.format(config.TMP_PATH, frame_id)
        pathor = Pathor(frame_id)

        self.assertEqual(pathor.ways, '{}ways.txt'.format(working_dir))
        self.assertEqual(pathor.image, '{}image.png'.format(working_dir))
        self.assertEqual(pathor.frame, '{}frame.png'.format(working_dir))
        self.assertEqual(pathor.label, '{}label.png'.format(working_dir))
        self.assertEqual(pathor.encoded_frame, '{}encoded_frame'.format(
            working_dir))
