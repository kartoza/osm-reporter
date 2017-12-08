[![Stories in Ready](https://badge.waffle.io/timlinux/osm-reporter.png?label=ready)](https://waffle.io/timlinux/osm-reporter)

# A simple tool for getting stats for an openstreetmap area.

See http://linfiniti.com/2012/12/holiday-openstreetmap-project-for-swellendam/

You can also use this tool to download OSM shapefiles with a nice QGIS canned
style for OSM roads and buildings for the area of your choosing.

# Install

# Docker install

This will install and setup a postgis (kartoza/postgis) and an osm-reporter
(kartoza/osm-reporter) container and then run the application with the source
code from osm-reporter mounted into the osm-reporter container.

```
sudo apt-get install python-pip git
sudo pip install docker-compose
git clone git://github.com/kartoza/osm-reporter.git
cd osm-reporter
# "make up" is an alias for the following command
docker-compose up -d web
```

If you like you can change the port number in the docker compose and run the site behind an nginx reverse proxy (or apache2 if you prefer) pointing to the running container. e.g. check `deployment/nginx/osm.inasafe.org.nginx.conf`:

**Note:** See our troubleshooting section below if running on docker.

# Manual Install for deployment

Prerequisites:

    sudo apt-get install osm2pgsql postgis

Or under MacOS:

    brew install osm2pgsql

If you install Postgres9.4.app you will get ``pgsql2shp`` on MacOS.

Ensure that the above binaries are in your path. If running on MacOS you
will need to ensure that ``/Applications/Postgres94.app/Contents/MacOS/bin/``
is in the path of the user running the server.

You should also give the process that osm-reporter runs as createdb rights
(needed to support the shape downloading feature). You should also have a
postgis template named 'template_postgis' available on your system. Consult a
postgis tutorial online to see how this is done. An example of setting this up
under MacOS is provided below:

    export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/
    psql

Now execute the following commands to create the template_postgis database:

    create database template_postgis encoding 'UTF8' TEMPLATE template0;
    update pg_database set datistemplate=true where datname='template_postgis';


Now execute the following bash commands to load the required legacy postgis
support:

    psql template_postgis < "create extension postgis;"
    psql template_postgis < /Applications/Postgres.app/Contents/Versions/9.4/share/postgresql/contrib/postgis-2.1/legacy_minimal.sql
    psql template_postgis < /Applications/Postgres.app/Contents/Versions/9.4/share/postgresql/contrib/postgis-2.1/legacy_gist.sql



First clone:

    cd /home/web
    git clone git://github.com/timlinux/osm-reporter.git

Then setup a venv (you may need to adjust the path to your python3
executable):

    cd osm-reporter
    virtualenv -p /usr/local/bin/python3.6 venv
    source venv/bin/activate
    pip3 install -r requirements.txt

Then deploy under apache mod_wsgi:

    cd apache
    cp osm-reporter.apache.conf.templ osm-reporter.apache.conf

Modify the contents of osm-reporter.apache.conf to suite your installation. Then do :

    sudo apt-get install libapache2-mod-wsgi
    cd /etc/apache/sites-available
    sudo ln -s /home/web/osm-reporter/apache/osm-reporter.apache.conf .
    sudo a2ensite osm-reporter.apache.conf

The default configuration assumes a user named 'osm-reporter' exists on your
system that the wsgi process will run under. If you wish to follow this
convention you should create the user:

    sudo useradd osm-reporter

And also give that user a database account (needed for the shape download
feature) and database create permissions:

    createuser osm-reporter
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) y
    Shall the new role be allowed to create more new roles? (y/n) n

If deploying locally you can leave the apache conf file mostly unchanged and
add this to your /etc/hosts file:

    127.0.0.1       osm-reporter.localhost

Next restart apache:

    sudo service apache2 restart

Now test - open chrome and visit: http://osm-reporter.localhost

# Manual install for development

Follow the install above and stop after setting up a venv.
You don't need to configure apache, there is a lightweight development web server.
You can run it:

    python runserver.py

and then visit http://127.0.0.1:5000/

*Note*: If running under PyCharm on MacOS, ensure that your run configuration
includes the following:

* *Script:* ``/Users/timlinux/dev/python/osm-reporter/runserver.py``
* *Environment:* ``PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/;PYTHONUNBUFFERED=1``
* *Working directory:* ``/Users/timlinux/dev/python/osm-reporter/``

(Update these paths as needed to match your system)

* Logging

OSM-Reporter will log requests as geojson files - one file per request.
The attributes of each geojson file will contain the following:

* feature_type (building, roads etc.)
* qgis_version
* inasafe_version (if applicable)
* year / month / day / hour of request
* bounding box of request as a GeoJSON geometry

You can use [geojson-merge](https://github.com/mapbox/geojson-merge) to
combine these into a single file (e.g. for use in QGIS). We assume you
have npm installed):

```
npm install --upgrade -g @mapbox/geojson-merge
geojson-merge 2017**.geojson > combined.geojson
```

Where the above example would merge all log files from 2017 into a
single log file.

# Config

You can optionally define a 'config' python module to override the default
behaviour of *OSM-Reporter*.

You can create the python module wherever you want, and then you will need to add
the environment var `REPORTER_CONFIG_MODULE` to make `reporter` aware of
it. For example:

    export REPORTER_CONFIG_MODULE="path.to.the.module"

Then you can override the config properties to fit your needs. Note that you
can override only the properties you need to, the others will fallback to
default values. For inspiration, you can have a look at
:file:`reporter/config/default.py`

**Available config**


CREW:

    (list) valid OSM users names of people actively working on your data
        gathering project. When set, an additional tag will be added
        in the user profile areas to indicate those who are crew members.

BBOX:

    (str) default bbox to use for the map and the stats;
        format is: "{SW_lng},{SW_lat},{NE_lng},{NE_lat}

DISPLAY_UPDATE_CONTROL:

    (bool) either to display or not the "update stats" button on the map

CACHE_DIR:

    (str) path to a dir where to cache the OSM files used by the backend

LOG_DIR:

    (str) path to a dir where to store request logs in geojson format

TAG_NAMES: (**TODO - verify if this is actually used.**)

    (list) tag names available for stats (default: ['building', 'highway'])

OSM2PGSQL_OPTIONS :
    (str) options for the osm2pgsql command line

**Setting config using environment variables**

All of the above configuration options can also be managed by
setting them as environment variables. e.g.

```
CREW=timlinux,gustry python runserver.py
```

Would run the application with a specific list of users in crew.


# Osm2pgsql

On some computers with less RAM than servers, you may adapt the import into postgis with osm2pgsql.
For instance in your 'config' python module above :

    OSM2PGSQL_OPTIONS = '--cache-strategy sparse -C 1000'

# Tests and QA

There is a test suite available, you can run it using nose e.g.:

    PYTHONPATH=`pwd`/reporter:`pwd`:${PYTHONPATH} nosetests -v --with-id \
    --with-xcoverage --with-xunit --verbose --cover-package=reporter reporter

On MacOS

Assumptions:

* You have chrome installed
* You have brew installed
* You have postgres.app installed

For selenium tests you need to install chromedriver:

    brew install chromedriver

And ensure that the chromedriver executable is in your path:

    export PATH=$PATH:/usr/local/bin/chromedriver

(If you are using pycharm you could add this path to your test runner
configuration.)

Before you run the tests, be sure to launch the chromedriver:

    chromedriver

Brew installation of chromedriver will also give you notes on how to
run this via launchd if you do not feel inclined to start chromedriver
each time.

Ensure you have your template_postgis etc. set up (described further up in
this document) and that your path includes the Postgres.app bin directory:

    export PYTHONPATH=`pwd`/reporter:`pwd`:$PYTHONPATH:venv/lib/python2.7/site-packages/; \
    nosetests -v --with-id  --with-xunit --verbose --cover-package=reporter reporter

Using Docker

    docker-compose build test
    docker-compose run test

# Continuous integration

* Current test status master: [![Build Status](https://travis-ci.org/kartoza/osm-reporter.svg?branch=master)](https://travis-ci.org/kartoza/osm-reporter) and
[![Code Health](https://landscape.io/github/kartoza/osm-reporter/master/landscape.svg?style=flat)](https://landscape.io/github/kartoza/osm-reporter/master)

* Current test status develop: [![Build Status](https://travis-ci.org/kartoza/osm-reporter.svg?branch=develop)](https://travis-ci.org/kartoza/osm-reporter) and
[![Code Health](https://landscape.io/github/kartoza/osm-reporter/develop/landscape.svg?style=flat)](https://landscape.io/github/kartoza/osm-reporter/develop)

# Local file instead of Overpass API

* Download PBF file from the internet
* Rename it `data.pbf` and put it in the root folder `osm-reporter/reporter/resources/pbf/`.
* OSM-Reporter will now skip Overpass and use this local OSM file.
Be careful to download data which are included in your PBF file. The BBOX parameter will not be parsed.

# Sentry

Sentry is a service that collects exceptions and displays aggregate reports
for them. You can view the sentry project we have running for osm-reporter
here: http://sentry.kartoza.com/osm-reporter/

# Troubleshooting


**Issue:** I deployed under docker and it seems my disk is filling up with the container.

**Answer:** Although the application is stateless, if keeps lots of logs. If your deployment gets lots of traffic those logs in docker can consume lots of disk space. As a short term fix you can simple remove the container and redeploy:

```
root@osm ~/osm-reporter # docker-compose kill
Killing osmreporter_web ... done
Killing osmreporter_db ... done
root@osm ~/osm-reporter # docker-compose rm
Going to remove osmreporter_web, osmreporter_db
Are you sure? [yN] y
Removing osmreporter_web ... done
Removing osmreporter_db ... done
root@osm ~/osm-reporter # df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3.9G     0  3.9G   0% /dev
tmpfs           799M   84M  716M  11% /run
/dev/sda1       188G  5.3G  173G   3% /
tmpfs           3.9G   80K  3.9G   1% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           3.9G     0  3.9G   0% /sys/fs/cgroup
tmpfs           799M     0  799M   0% /run/user/0
root@osm ~/osm-reporter # docker-compose up -d web
```


Tim Sutton, Etienne Trimaille & Yohan Boniface
