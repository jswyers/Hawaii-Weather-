import matplotlib
matplotlib.use('nbagg')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import and_


# Reflect Database into ORM class
engine = create_engine("sqlite:///hawaii.sqlite") 
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.stations


session = Session(engine)    

from flask import Flask, jsonify

# Create an app
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br>"
        f"/api/v1.0/<start_date>/<end_date>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_rain = session.query(Measurement.date, Measurement.prcp).\
        filter(and_(Measurement.date >= "2016-08-21", Measurement.date <= "2017-08-21")).all()
    yr_dict = dict(year_rain)

    return jsonify(yr_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_list = session.query(Measurement.date, Measurement.tobs).\
        filter(and_(Measurement.date >= "2016-08-21", Measurement.date <= "2017-08-21",Measurement.station == 'USC00519281')).all()
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def start_only(start_date):
    just_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    return jsonify(just_start)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):
    st_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(st_end)

if __name__ == "__main__":
    app.run(debug=True)