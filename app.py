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
Measurement = Base.classes.measurement

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
        f"/api/v1.0/measurement<br/>"
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

@app.route("/api/v1.0/measurement")
def measurement():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()

    session.close()

    all_measurement = []
    for station, date, prcp, tobs in results:
        measurement_dict = {}
        measurement_dict["station"] = station
        measurement_dict["name"] = name
        measurement_dict["latitude"] = latitude
        measurement_dict["longitude"] = longitude
        
        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)

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

@app.route('/api/v1.0/<startdate>')
def start_date(startdate):
    
    # """Fetch data from start date to end.  
    # Start date needs to be YYYY-MM-DD"""
    

    results = engine.execute(f"""SELECT date,
                                        MIN(tobs) AS tmin,
                                       AVG(tobs) AS tavg,
                                       MAX(tobs) AS tmax
                                FROM measurement
                                WHERE date >= '{startdate}'
                                GROUP BY date
                            """)
    all_start = []
    for date, tmin, tavg, tmax in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["tmin"] = tmin
        start_dict["tavg"] = tavg
        start_dict["tmax"] = tmax

        all_start.append(start_dict)

    return jsonify(all_start)


@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end(start_date,end_date):
    
    # """Fetch data from start date to end.  
    # Start date needs to be YYYY-MM-DD"""

    run_sql = f"""SELECT date,
                    MIN(tobs) AS tmin,
                    AVG(tobs) AS tavg,
                    MAX(tobs) AS tmax
                    FROM measurement
                    WHERE date BETWEEN '{start_date}' AND '{end_date}'
                    GROUP BY date
                """
    
    # print("run_sql:", run_sql)

    results = engine.execute(run_sql)
    
    all_start_end = []
    for date, tmin, tavg, tmax in results:
        start_end_dict = {}
        start_end_dict['date'] = date
        start_end_dict["tmin"] = tmin
        start_end_dict["tavg"] = tavg
        start_end_dict["tmax"] = tmax

        all_start_end.append(start_end_dict)
    
    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True, port=5009)