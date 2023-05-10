from os import stat
import numpy as np
import pandas as pd
import json
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from scipy import stats

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine(f"sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    """List of all available api paths."""
    return(
        f"Homepage<br/>"
        f"<br/>Available Paths:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<br/><br/>Enter date ranges below (YYYY-MM-DD):<br/>"
        f"(2010-01-01 to 2017-08-23)<br/><br/>"
        f"<br/>/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date"
        f"<br/><br/><br />Example:<br/>"
        f"<a href='/api/v1.0/2012-06-12'>/api/v1.0/2012-06-12</a><br/>"
        f"<a href='/api/v1.0/2012-06-12/2016-05-18'>/api/v1.0/2012-06-12/2016-05-18/</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Query precipitation
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    precipitation_list = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        precipitation_list.append(precipitation_dict)
    
    # return data from list in JSON 
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station
    stations = session.query(station.id, station.station, station.name).all()

    session.close()
    
    all_stations = list(np.ravel(stations))
    
    # return data in JSON 
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # query to find the most active station (most rows), and list in descending order.
    # Take the first station reading and store in variable
    ddd = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station)\
        .order_by(func.count(measurement.station).desc()).first()
    
    most_station = ddd[0]

    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # query to find date and temperature data from previous year, after 2016-08-18 for most active station "USC00519281"
    tobs = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station==most_station).\
        filter(measurement.date >= last_year).\
        order_by(measurement.date).all()

    session.close()

    # create list comprehension for date, temperature
    temp_date = [result[0] for result in tobs]
    temp_data = [result[1] for result in tobs]

    # place data in pd.DataFrame 
    temp_df = pd.DataFrame({
            "Date": temp_date, 
            "Temperature": temp_data})

    # load dataframe as JSON 
    temp_df = json.loads(temp_df.to_json(orient='records'))

    # return dictionary with key containing each date, temperature data in JSON 
    return jsonify(temp_df)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # create a query to list all dates from Measurement
    dates = session.query(measurement.date)
    
    session.close()
    
    date_list =[date[0] for date in dates]

    # check if start date in date_list 
    if start in date_list:

        # perform calculation using query 
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

        # create empty list to store results
        result_calculations = []

        # create dictionary for results
        for min, avg, max in results:
            calculation_start = {}
            calculation_start["Minimum Temperature"] = min
            calculation_start["Avg Temperature"] = avg
            calculation_start["Max Temperature"] = max
            result_calculations.append(calculation_start)
        
        # return results in JSON
        return jsonify(result_calculations)

    # return error message if start date not in dates database
    else:
        return jsonify({"error": f"Start Date on {start} not found."}), 404



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # create a query to list all dates from Measurement
    dates = session.query(measurement.date)
    date_list =[date[0] for date in dates]

    # check if start and end date in date_list 
    if start in date_list and end in date_list:

        # perform calculation 
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()

        # create empty list to store results
        final_calculations = []

        # create dictionary for results
        for min, avg, max in results:
            calculation_dict = {}
            calculation_dict["Minimum Temperature"] = min
            calculation_dict["Avg Temperature"] = avg
            calculation_dict["Max Temperature"] = max
            final_calculations.append(calculation_dict)

            # return results in JSON
            return jsonify(final_calculations)
    
    # return error message if start date or end date not in dates database
    else: 
        return jsonify({"error": f"Start Date on {start} or End Date {end} not found."}), 404 


if __name__ == '__main__':
    app.run(debug=True)
