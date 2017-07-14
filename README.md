# GTFS viewer for matka.fi dump

Functions that are used for reading GTFS are from this repository https://github.com/afimb/gtfslib-python

# Used technologies

- Python
- jQuery
- Tornado (web server)
- gtfslib-python (reads GTFS to db + extra functionalities)
- sqlite3
- Leaflet

# Usage / install

1. GTFS file has to be unzipped and added to the database by running the following command in python dao.load_gtfs(your_zip_file)
2. After forming database it can be accessed by dao = Dao("db.sqlite")
3. You can run it from main.py (cmd: python main.py)
