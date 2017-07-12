"""
Definition of classes representing tables in the database
"""

import MySQLdb
import config


def _saveToDB (sqlQuery) :
    # This opens and closes the connections to the database.
    # Since writings occur only every 10 minutes it wouldn't be efficient to
    # let the connection open.

    db = MySQLdb.connect(
        host=config.db_host, db=config.db_name, user=config.db_user, passwd=config.db_password)
    print("[_saveToDB] DEBUG " + sqlQuery)
    cur = db.cursor()
    cur.execute(sqlQuery)

    db.close()

class Measurement () :
    """
    One measurement made by the water sensor
    """

    def __init__ (self, packetNr, reservoir, waterLevel, conductivity, salinity, tds, pH) :
        self.packetNr     = packetNr
        self.reservoir    = reservoir
        self.waterLevel   = waterLevel
        self.pH           = pH
        self.conductivity = conductivity
        self.salinity     = salinity
        self.tds          = tds

    def __str__ (self) :
        return "reservoir={}, waterLevel={}, pH={}, conductivity={}, salinity={}, tds={}".format(
            self.reservoir, self.waterLevel, self.pH,
            self.conductivity, self.salinity, self.tds)
    
    def save (self) :
        """
        Save this measurement to the database.
        """
        
        try:
            sqlQuery = """
            INSERT INTO {} (packetNr, waterLevel, pH, conductivity, reservoir_id, dateTime, salinity, tds) 
            VALUES ({}, {}, {}, {}, {}, now(), {}, {})
            """.format(
                config.db_measur_table_name,
                self.packetNr,
                self.waterLevel,
                self.pH,
                self.conductivity,
                self.reservoir,
                self.salinity,
                self.tds)

            _saveToDB(sqlQuery)
        except Exception as e:
            print('[Measurement#save] failed to save instance: {}'.format(e))