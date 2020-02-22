#################################################
# Import Dependencies
#################################################

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
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
        f"Available Routes:<br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/stations'>/api/v1.0/stations</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/tobs'>/api/v1.0/tobs</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/2016-07-29'>/api/v1.0/&lt;start date &gt;</a>            use date format:YYYY-MM-DD <br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/2016-07-29/2017-07-29'>/api/v1.0/&lt;start date &gt;/&lt;end date&gt;</a>      use date format:YYYY-MM-DD"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and precipitations"""
    # Query all precipitations
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_date_prcp = []
    for date,precip in results:
        date_dict = {}
        date_dict[date] = precip
        all_date_prcp.append(date_dict)

    return jsonify(all_date_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#query for the dates and temperature observations from a year from the last data point.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs (temperature observations) for the last year of data in the table"""
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= query_date).all()
        
    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


# Create function to validate input as specific date format YYYY-MM-DD
def validate(date_text):
    try:
        dt.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<startDate>")
def temp_date_end(startDate):
    """Fetch the TMIN, TAVG and TMAX given a  start/end date
       variables supplied by the user, or a 404 if not."""
    
    if isinstance(startDate,str):
        print(f"One date passed - Determine agg funcs over date range")
        validate(startDate)
        # Create our session (link) from Python to the DB
        session = Session(engine)

        results = session.query(func.min(Measurement.tobs),\
                                func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).\
                                filter(Measurement.date >= startDate).first()
        
        session.close()

        # Convert list of tuples into normal list
        temps_agg = list(np.ravel(results))

        return jsonify(temps_agg)
    return jsonify({"error": "Dates not found."}), 404

# When given the start and end dates separated by a "/", calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<startDate>/<endDate>")
def temp_date_range(startDate,endDate):
    """Fetch the TMIN, TAVG and TMAX given a  start/end date
       variables supplied by the user, or a 404 if not."""
    
    if isinstance(endDate,str):
        print(f"Both Dates passed - Determine agg funcs over date range")
        validate(startDate)
        validate(endDate)
        # Create our session (link) from Python to the DB
        session = Session(engine)

        results = session.query(func.min(Measurement.tobs),\
                                func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).\
                                filter(Measurement.date >= startDate).\
                                filter(Measurement.date <= endDate).first()
        
        session.close()

        # Convert list of tuples into normal list
        temps_agg = list(np.ravel(results))

        return jsonify(temps_agg)
    return jsonify({"error": "Dates not found."}), 404








if __name__ == '__main__':
    app.run(debug=True)