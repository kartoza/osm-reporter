import os
from reporter.test.logged_unittest import LoggedTestCase
from reporter.test.helpers import (
    UNKNOWN_OSMFILE_PATH,
    SWELLENDAM_OSMFILE_PATH
)
from reporter.animate.osm_data import (
    OsmData,
    snap_datamap
)
# from reporter.utilities import LOGGER
from reporter import config


class OsmDataTestCase(LoggedTestCase):

    def test_with_unknown_osm_file(self):
        """
        When the OSM file does not exist
        It should assigns None to
        ways, bounds and datamap
        """
        osm_file = UNKNOWN_OSMFILE_PATH
        data = OsmData(osm_file)
        self.assertEqual(data.ways, None)
        self.assertEqual(data.bounds, None)
        self.assertEqual(data.datamap, None)

    def test_with_known_osm_file_with_bounds(self):
        """
        When the OSM file exists
        It should parse the OSM file
        to retrieve an array of <way> tags
        and a map of the <bounds> tag.
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        data = OsmData(osm_file)
        expected_way_count = 333
        expected_bounds = {
            "minlat": "-34.0537260",
            "minlon": "20.4114820",
            "maxlat": "-34.0094830",
            "maxlon": "20.4673580"
        }
        self.assertEqual(len(data.ways), expected_way_count)
        self.assertEqual(data.bounds["minlat"], expected_bounds["minlat"])
        self.assertEqual(data.bounds["minlon"], expected_bounds["minlon"])
        self.assertEqual(data.bounds["maxlat"], expected_bounds["maxlat"])
        self.assertEqual(data.bounds["maxlon"], expected_bounds["maxlon"])

    def test_map_ways_for_frame(self):
        """
        It should find 9 <way> ids for the frame '2010-01'
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        data = OsmData(osm_file)

        frame = '2010-01'
        ways = data.map_ways_for_frame(frame)
        self.assertEqual(len(ways), 9)
        self.assertEqual(ways[0], '47587914')

    def test_filter_coordinates(self):
        """
        It should find 9 coordinates for the frame '2010-01'
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        data = OsmData(osm_file)

        frame = '2010-01'
        coordinates = data.filter_coordinates_for_frame(frame)
        expected_coordinates = '-34.029976,20.431830 -34.030593,20.432838' + \
            ' -34.030990,20.433494 // id=47587914;highway=residential;' + \
            'name=Maynier Street\n'
        self.assertEqual(len(coordinates), 9)
        self.assertEqual(coordinates[0], expected_coordinates)

    def test_frames(self):
        """
        It should return 32 frames from this OSM file
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        data = OsmData(osm_file)

        frames = data.frames()
        self.assertEqual(frames[0], '2010-01')
        self.assertEqual(len(frames), 32)

    def test_snap_datamap_from_known_osm_file(self):
        """
        It should snap an OSM file
        """
        osm_file = SWELLENDAM_OSMFILE_PATH
        datamap = snap_datamap(osm_file)

        # check the datamap file exists
        self.assertTrue(os.path.exists(config.DATAMAP))

        # check the datamap file's first line
        expected_datamap = '-34.026440,20.448198 -34.026266,20.448653 ' + \
            '-34.025996,20.449497 -34.025467,20.451333' + \
            ' -34.024931,20.453213 -34.024680,20.454165' + \
            ' -34.024562,20.454708 -34.024493,20.455156 ' + \
            '-34.024379,20.456064 -34.024148,20.458149' + \
            ' // id=4361694;highway=trunk;oneway=no;ref=N2\n'
        self.assertEqual(datamap[0], expected_datamap)

    def test_snap_datamap_from_unkwnwn_osm_file(self):
        """
        It should return None as the osm file does not exist
        """
        osm_file = UNKNOWN_OSMFILE_PATH
        datamap = snap_datamap(osm_file)

        # check that the datamap file does not exist
        self.assertFalse(os.path.exists(config.DATAMAP))

        # check that datamap returns None
        self.assertIsNone(datamap)
