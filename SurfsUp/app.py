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
        f"/api.v1.0/stations<br />"
        f"/api.v1.0/tobs<br />"
        f"/api.v1.0/<start><br />"
        f"/api.v1.0/<start>/<end><br />"
          
    )

# Create precipitation routes for the last 12 months 
@app.route("/api.v1.0/precipitation")
def raining():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).order_by(Measurement.date).all()

    # 2.Convert results to a dict with date as key and prcp as value
    result_dict = dict(results)
    session.close()

    # 2. return the json representation of your dictionary
    return jsonify(result_dict)

    # 3. Create the station route of a list of the stations from the dataset
app.route("/api/v1.0/stations")

def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
        group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    #Convert results to a dict
    stations_dict = dict(stations)
    session.close()

    # Return the json representation of your dictionary
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")

def tobs():
    max_temp_obs = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
 
    # Create dict
    tobs_dict = dict(max_temp_obs)
    session.close()

    # Return Json representation of the dict
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")


def start(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                           func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    #Create an empty list to hold values
    temp_stats = []
    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        temp_stats.append(tobs_dict)
    return jsonify(temp_stats) 
@app.route('/api/v1.0/<start>/<end>')

def start_end(start,end):
    start_ending = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                           func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    #Create an empty list to hold values
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