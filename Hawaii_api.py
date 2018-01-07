import pandas as pd
from datetime import datetime


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()
session = Session(engine) 

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the stations class to a variable called `stations`
stations = Base.classes.stations

# Assign the measurements class to a variable called `measurements`
measurements = Base.classes.measurements

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    "List all available api routes."
    return (
        f"""Available Routes:</br>
        /api/v1.0/precipitation</br>
        /api/v1.0/stations</br>
        /api/v1.0/tobs</br>
        input &ltstart&gt and &ltend&gt in format %Y-%M-%D </br>
        /api/v1.0/&ltstart&gt</br>
        /api/v1.0/&ltstart&gt&&ltend&gt</br>"""
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    "Return a list of temperature observations from the last year"
    # Query for the dates and temperature observations from the last year
    #results = session.query("measurements.date, measurements.tobs WHERE date >= datetime('2017-08-23', '-12 months')")
    #results = session.query(measurements).all()

    results = session.query(measurements).filter(measurements.date.between('2016-08-23', '2017-08-23'))
    # Create a dictionary from the row data and append to a list of tobs
    tobs = []
    for temp in results:
        temp_dict = {}
        temp_dict[temp.date] = temp.tobs
        tobs.append(temp_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/stations")
def stationista():
    "Return a json list of stations from the dataset."
    # Query for the dates and temperature observations from the last year
    results = session.query(stations).all()
    
    all_stations = [x.station for x in results]

    return jsonify(all_stations)

@app.route("/api/v1.0/<selected_start>")
def start(selected_start):
    "When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."
    # minimumm = session.query("SELECT tobs FROM measurements WHERE date >= datetime('" + start + "') ORDER BY tobs ASC LIMIT 1").fetchone()[0]
    # maximum = session.query("SELECT tobs FROM measurements WHERE date >= datetime('" + start + "') ORDER BY tobs DESC LIMIT 1").fetchone()[0]
    # average = session.query("SELECT ROUND(AVG(tobs)) FROM measurements WHERE date date >= datetime('" + start + "') ORDER BY tobs DESC LIMIT 1").fetchone()[0]

    
    minimum = session.query(measurements.tobs, func.min(measurements.tobs)).filter(measurements.date >= selected_start)
    maximum = session.query(measurements.tobs, func.max(measurements.tobs)).filter(measurements.date >= selected_start)
    average = session.query(measurements.tobs, func.avg(measurements.tobs)).filter(measurements.date >= selected_start)

    start_temp = {"Tmin": minimum[0][0], "Tmax": maximum[0][0], "Tavg": average[0][0]}

    return jsonify(start_temp)

    @app.route("/api/v1.0/<selected_start>&<selected_end>")
    def start(selected_start, selected_end):
        "When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."
        minimum = session.query(measurements.tobs, func.min(measurements.tobs)).filter(measurements.date.between(selected_start, selected_end))
        maximum = session.query(measurements.tobs, func.max(measurements.tobs)).filter(measurements.date.between(selected_start, selected_end))
        average = session.query(measurements.tobs, func.avg(measurements.tobs)).filter(measurements.date.between(selected_start, selected_end))

        start_end_temp = {"Tmin": minimum[0][0], "Tmax": maximum[0][0], "Tavg": average[0][0]}

        return jsonify(start_end_temp)




if __name__ == '__main__':
    app.run(debug=True)

