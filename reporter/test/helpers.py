# coding=utf-8
"""Helpers for tests.
:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""

import os

FIXTURE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_data',
    'swellendam.osm'
)

UNKNOWN_OSMFILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_data',
    'unknown_osm_file.osm'
)

SWELLENDAM_OSMFILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_data',
    'swellendam_with_bounds.osm'
)

WAYS_FILE = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
  'ways.txt')

BIG_IMAGE = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
  'big_image.png')

TMP_BIG_IMAGE = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
  'tmp_big_image.png')

SMALL_IMAGE = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
  'small_image.png')

TMP_SMALL_IMAGE = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
  'tmp_small_image.png')
