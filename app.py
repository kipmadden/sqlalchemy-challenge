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
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start date YYYY-MM-DD &gt;<br>"
        f"/api/v1.0/&lt;start date YYYY-MM-DD &gt;/&lt;end date&gt;"
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

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>/<end>")
def temp_date_range(startDate,endDate):
    """Fetch the TMIN, TAVG and TMAX given a start date or start/end date
       variables supplied by the user, or a 404 if not."""
    # Create function to reject non-date inputs
    def validate(date_text):
        try:
          dt.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
          raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    
    if endDate:
        print(f"Both Dates passed - Determine agg funcs over date range")
        validate(startdate)
        validate(endDate)
           # Create our session (link) from Python to the DB
            session = Session(engine)

            """Return a list of tobs (temperature observations) for the last year of data in the table"""
            query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

            results = session.query(func.min(Measurement.tobs),\
                                    func.avg(Measurement.tobs),\
                                    func.max(Measurement.tobs)).\
                                    filter(Measurement.date >= queryDate).\
                                    filter(Measurement.date <= endDate).all()
            
            session.close()

            # Convert list of tuples into normal list
            temps_agg = list(np.ravel(results))

            return jsonify(temps_agg)
    else:
        print(f"Only startDate passed - Determine agg funcs >= startDate")
    canonicalized = superhero.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["superhero"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": "Character not found."}), 404




if __name__ == '__main__':
    app.run(debug=True)