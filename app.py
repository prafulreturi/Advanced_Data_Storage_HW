import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///hawaii.sqlite")
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
def welcome():
    """List all available api routes."""
    return (
         f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end></br>"
    )


begin_date = dt.date(2016, 8, 23)

@app.route("/api/v1.0/precipitation")

def precipitation():
    
    # retrieve the last 12 months of precipitation data
    
 results = session.query(Measurement.date, Measurement.prcp).\
                         filter(Measurement.date >= begin_date).\
                         order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
 last_12mnths_prcp = []
 for precipitation in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = precipitation.date
        precipitation_dict["Precipitation"] = precipitation.prcp
        last_12mnths_prcp.append(precipitation_dict)
        

 return jsonify(last_12mnths_prcp)

@app.route("/api/v1.0/stations")

def stations():
    
    # Query all the stations

 results = session.query(Station).all()

    # Create a dictionary from the row data and append to a list of all_stations.

 all_stations = []
 for station in results:
        stations_dict = {}
        stations_dict["Station"] = station.station
        stations_dict["Station Name"] = station.name
        stations_dict["Latitude"] = station.latitude
        stations_dict["Longitude"] = station.longitude
        stations_dict["Elevation"] = station.elevation
        all_stations.append(stations_dict)
    
 return jsonify(all_stations)

@app.route("/api/v1.0/tobs")

def tobs():
    
    # Query all the stations and for the given date. 

 results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                    group_by(Measurement.date).\
                    filter(Measurement.date > begin_date).\
                    order_by(Measurement.station).all()
                    
    # Create a dictionary from the row data and append to a list of for the temperature data.

 all_temp = []
 for tob in results:
        tobs_dict = {}
        tobs_dict["Station"] = tob.station
        tobs_dict["Date"] = tob.date
        tobs_dict["Temperature"] = tob.tobs
        all_temp.append(tobs_dict)
    
 return jsonify(all_temp)

@app.route("/api/v1.0/<start>")

def start_date_stats(start):
    
    # Query all the stations and for the given date. 

 results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of for the temperature data.
 start_temp_stats = []
    
 for tmin, tmax, tavg in results:
        temp_dict = {}
        temp_dict["Minimum Temp"] = tmin
        temp_dict["Maximum Temp"] = tmax
        temp_dict["Average Temp"] = tavg
        start_temp_stats.append(temp_dict)
    
 return jsonify(start_temp_stats)
    

@app.route("/api/v1.0/<start>/<end>")

def start_end_stats(start, end):
    
    
    # Query all the stations and for the given range of dates. 

 results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of for the temperature data.
 start_end_stats = []
    
 for tmin, tmax, tavg in results:
        start_end_dict = {}
        start_end_dict["Minimum Temp"] = tmin
        start_end_dict["Maximum Temp"] = tmax
        start_end_dict["Average Temp"] = tavg
        start_end_stats.append(start_end_dict)
    
 return jsonify(start_end_stats)

if __name__ == '__main__':
    app.run(debug=True)
