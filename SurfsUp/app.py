"""
Part 2: Design Your Climate App
Now that you’ve completed your initial analysis, 
you’ll design a Flask API based on the queries that you just developed. 
To do so, use Flask to create your routes as follows:
"""
# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, Request, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def main():
    return(
        f"Climate changes in Hawaii<br />"
        f"Available Routes<br />"
        f"Rainfall from last year: /api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f" /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
          
    )

# precipitation route 
# Create precipitation routes for the last 12 months 
@app.route("/api/v1.0/precipitation")
def raining():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).order_by(Measurement.date).all()
    result_dict = dict(results)
    session.close()
    return jsonify(result_dict)

# station route
# Returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    result= session.query(Station.station).all()
    session.close()
    station_name= list(np.ravel(result))
    return jsonify (station_name)

#  tobs route Returns jsonified data for the most active station (USC00519281) 
#  Only returns the jsonified data for the last year of data 
@app.route("/api/v1.0/tobs")
def tobs():
    max_temp_obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23').all()
 
    tobs= list(np.ravel(max_temp_obs))
    session.close()
    return jsonify(tobs)

# A start route that accepts the start date as a parameter from the URL
# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset 
@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                           func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
  
    temp_stats = []
    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        temp_stats.append(tobs_dict)
    return jsonify(temp_stats) 

# start/end route that accepts the start and end dates as parameters from the URL 
# Returns the min, max, and average temperatures calculated from the given start date to the given end date 
@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    start_ending = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                           func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    all_stats = []
    for min, avg, max in start_ending:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        all_stats.append(tobs_dict)
    return jsonify(all_stats) 
   
if __name__ == "__main__":
      app.run(debug = True)