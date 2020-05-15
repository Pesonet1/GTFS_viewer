# GTFS viewer for matka.fi dump

Tool for viewing & reading GTFS file

## Used libraries

* Python (tornado, psycopg2, zc.buildout)
* gtfslib-python for sqlite3
* gtfsdb for PostgreSQL
* jQuery
* Leaflet (Leaflet.markercluster, Leaflet-color-markers)
* Moment
* Bootstrap

## Install

1. Install python packages
  * tornado, psycopg2, zc.buildout
  * `$ pip install <package-name>`
2. Install gtfslib-python
  * git clone https://github.com/afimb/gtfslib-python
  * `$ pip install .`
3. Install gtfsdb https://github.com/OpenTransitTools/gtfsdb
  * git clone
  * `$ buildout install prod`
4. Load GTFS dump from [matka.fi](developer.matka.fi/pages/en/home.php)
5. (a) Initialize sqlite3 database with GTFS dump
  * Run `init_db.py` script by running `$ python init_db.py`
5. (b) Initialize PostgreSQL database with GTFS dump
  * Create database named `gtfs` into PostgreSQL
  * `./gtfsdb/bin/gtfsdb-load.exe --database_url postgresql://postgres:postgres@localhost:5432/gtfs <gtfs_dump_name>.zip`
  * This will take a while...
6. Run app
  * `$ python main.py`
  * Go to `http//localhost:5005/`
