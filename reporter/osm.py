# coding=utf-8
"""Module for low level OSM file retrieval.
:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""
import hashlib
import urllib2
import time
import os
import re
from subprocess import call
from shutil import copyfile

from .utilities import temp_dir, unique_filename, zip_shp, which
from . import config
from . import LOGGER
from queries import SQL_QUERY_MAP, OVERPASS_QUERY_MAP


def get_osm_file(coordinates, feature='all'):
    """Fetch an osm file given a bounding box using the overpass API.

    :param coordinates: Coordinates as a list in the form:
        [min lat, min lon, max lat, max lon]

    :param feature: The type of feature (buildings, building-points or roads).
    :type feature: str

    :returns: A file which has been opened on the retrieved OSM dataset.
    :rtype: file

        Coordinates look like this:
        {'NE_lng': 20.444537401199337,
         'SW_lat': -34.0460012312071,
         'SW_lng': 20.439494848251343,
         'NE_lat': -34.044441058971394}

                 Example overpass API query for buildings (testable at
            http://overpass-turbo.eu/)::

                (
                  node
                    ["building"]
                    ["building"!="no"]
                  ({{bbox}});
                  way
                    ["building"]
                    ["building"!="no"]
                  ({{bbox}});
                  rel
                    ["building"]
                    ["building"!="no"]
                  ({{bbox}});
                <;);out+meta;

    Equivalent url (http encoded)::
    """
    server_url = 'http://overpass-api.de/api/interpreter?data='
    query = OVERPASS_QUERY_MAP[feature].format(**coordinates)
    url_path = '%s%s' % (server_url, query)
    safe_name = hashlib.md5(query).hexdigest() + '.osm'
    file_path = os.path.join(config.CACHE_DIR, safe_name)
    return load_osm_document(file_path, url_path)


def load_osm_document(file_path, url_path):
    """Load an osm document, refreshing it if the cached copy is stale.

    To save bandwidth the file is not downloaded if it is less than 1 hour old.

    :param url_path: Path (relative to the ftp root) from which the file
        should be retrieved.
    :type url_path: str

    :param file_path: The path on the filesystem to which the file should
        be saved.
    :type file_path: str

    :returns: A file object for the the downloaded file.
    :rtype: file

     Raises:
         None
    """
    elapsed_seconds = 0
    if os.path.exists(file_path):
        current_time = time.time()  # in unix epoch
        file_time = os.path.getmtime(file_path)  # in unix epoch
        elapsed_seconds = current_time - file_time
        if elapsed_seconds > 3600:
            os.remove(file_path)
    if elapsed_seconds > 3600 or not os.path.exists(file_path):
        fetch_osm(file_path, url_path)
        message = ('fetched %s' % file_path)
        LOGGER.info(message)
    file_handle = open(file_path, 'rb')
    return file_handle


def fetch_osm(file_path, url_path):
    """Fetch an osm map and store locally.


    :param url_path: The path (relative to the ftp root) from which the
        file should be retrieved.
    :type url_path: str

    :param file_path: The path on the filesystem to which the file should
        be saved.
    :type file_path: str

    :returns: The path to the downloaded file.

    """
    LOGGER.debug('Getting URL: %s', url_path)
    request = urllib2.Request(url_path)
    try:
        url_handle = urllib2.urlopen(request, timeout=60)
        file_handle = file(file_path, 'wb')
        file_handle.write(url_handle.read())
        file_handle.close()
    except urllib2.URLError:
        LOGGER.exception('Bad Url or Timeout')
        raise


def add_keyword_timestamp(keywords_file_path):
    """Add the current date / time to the keywords file.

    :param keywords_file_path: Keywords file path that the timestamp should be
        written to.
    :type keywords_file_path: str
    """
    time_stamp = time.strftime('%d-%m-%Y %H:%M')
    keywords_file = file(keywords_file_path, 'ab')
    keywords_file.write('date: %s' % time_stamp)
    keywords_file.close()


def extract_shapefile(
        feature_type, file_path, qgis_version=2, output_prefix='', lang='en'):
    """Convert the OSM xml file to a shapefile.

    This is a multi-step process:
        * Create a temporary postgis database
        * Load the osm dataset into POSTGIS with osm2pgsql and our custom
             style file.
        * Save the data out again to a shapefile
        * Zip the shapefile ready for user to download

    :param feature_type: The feature to extract.
    :type feature_type: str

    :param file_path: Path to the OSM file name.
    :type file_path: str

    :param qgis_version: Get the QGIS version. Currently 1,
        2 are accepted, default to 2. A different qml style file will be
        returned depending on the version
    :type qgis_version: int

    :param output_prefix: Base name for the shape file. Defaults to ''
        which will result in an output file of feature_type + '.shp'. Adding a
        prefix of e.g. 'test-' would result in a downloaded file name of
        'test-buildings.shp'. Allowed characters are [a-zA-Z-_0-9].
    :type output_prefix: str

    :param lang: The language desired for the labels in the legend.
        Example : 'en', 'fr', etc. Default is 'en'.
    :type lang: str

    :returns: Path to zipfile that was created.
    :rtype: str

    """
    if not check_string(output_prefix):
        error = 'Invalid output prefix: %s' % output_prefix
        LOGGER.exception(error)
        raise Exception(error)

    output_prefix += feature_type

    # Extract
    work_dir = temp_dir(sub_dir=feature_type)
    directory_name = unique_filename(dir=work_dir)
    os.makedirs(directory_name)
    resource_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'resources', feature_type))
    style_file = os.path.join(resource_path, '%s.style' % feature_type)
    db_name = os.path.basename(directory_name)
    shape_path = os.path.join(directory_name, '%s.shp' % output_prefix)

    if qgis_version > 1:
        qml_source_path = os.path.join(
            resource_path, '%s-%s.qml' % (feature_type, lang))
        if not os.path.isfile(qml_source_path):
            qml_source_path = os.path.join(
                resource_path, '%s-en.qml' % feature_type)
    else:
        qml_source_path = os.path.join(
            resource_path, '%s-qgis1.qml' % feature_type)

    qml_dest_path = os.path.join(
        directory_name, '%s.qml' % output_prefix)

    keywords_source_path = os.path.join(
        resource_path, '%s-%s.keywords' % (feature_type, lang))
    if not os.path.isfile(keywords_source_path):
        keywords_source_path = os.path.join(
            resource_path, '%s-en.keywords' % feature_type)

    keywords_dest_path = os.path.join(
        directory_name, '%s.keywords' % output_prefix)
    license_source_path = os.path.join(
        resource_path, '%s.license' % feature_type)
    license_dest_path = os.path.join(
        directory_name, '%s.license' % output_prefix)
    prj_source_path = os.path.join(
        resource_path, '%s.prj' % feature_type)
    prj_dest_path = os.path.join(
        directory_name, '%s.prj' % output_prefix)
    # Used to standarise types while data is in pg still
    transform_path = os.path.join(resource_path, 'transform.sql')
    createdb_executable = which('createdb')[0]
    createdb_command = '%s -T template_postgis %s' % (
        createdb_executable, db_name)
    osm2pgsql_executable = which('osm2pgsql')[0]
    osm2pgsql_options = config.OSM2PGSQL_OPTIONS.encode(encoding='utf-8')
    osm2pgsql_command = '%s -S %s -d %s %s %s' % (
        osm2pgsql_executable,
        style_file,
        db_name,
        osm2pgsql_options,
        file_path)
    psql_executable = which('psql')[0]
    transform_command = '%s %s -f %s' % (
        psql_executable, db_name, transform_path)
    pgsql2shp_executable = which('pgsql2shp')[0]
    pgsql2shp_command = '%s -f %s %s %s' % (
        pgsql2shp_executable, shape_path, db_name, SQL_QUERY_MAP[feature_type])
    dropdb_executable = which('dropdb')[0]
    dropdb_command = '%s %s' % (dropdb_executable, db_name)
    # Now run the commands in sequence:
    print createdb_command
    call(createdb_command, shell=True)
    print osm2pgsql_command
    call(osm2pgsql_command, shell=True)
    print transform_command
    call(transform_command, shell=True)
    print pgsql2shp_command
    call(pgsql2shp_command, shell=True)
    print dropdb_command
    call(dropdb_command, shell=True)
    copyfile(prj_source_path, prj_dest_path)
    copyfile(qml_source_path, qml_dest_path)
    copyfile(keywords_source_path, keywords_dest_path)
    copyfile(license_source_path, license_dest_path)
    add_keyword_timestamp(keywords_dest_path)
    # Now zip it up and return the path to the zip, removing the original shp
    zipfile = zip_shp(shape_path, extra_ext=[
        '.qml', '.keywords', '.license'], remove_file=True)
    print 'Shape written to %s' % shape_path

    return zipfile


def check_string(text, search=re.compile(r'[^A-Za-z0-9-_]').search):
    """Test that a string doesnt contain unwanted characters.

    :param text: Text that you want to verify is compliant.
    :type text: str

    :param search: Regex to use to check the string. Defaults to allowing
        [^a-z0-9-_].

    :return: bool
    """
    return not bool(search(text))
