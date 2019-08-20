import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# # We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
# Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/precip<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/precip")
def precip():
    
    results = engine.execute("""SELECT date, 
                                       prcp 
                                FROM measurement
                                
    """)
    

    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        # precip_dict["date"] = date
        precip_dict[date] = prcp
        
        all_precip.append(precip_dict)
    
    
    return jsonify(all_precip)

@app.route("/api/v1.0/tobs")   
def tobs():
    results = engine.execute("""SELECT date, 
                                       tobs
                                       
                                FROM measurement
                                WHERE date >=  (SELECT date('2017-08-23', '-1 year'))   
                                    
                                

                                
    """)
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True, port=5009)