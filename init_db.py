from gtfslib.dao import Dao

dao = Dao('db.sqlite')
dao.load_gtfs('gtfs_new.zip')
