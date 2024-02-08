# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
def welcome():
    # List all available api routes.
    return (
        f"Welcome to the Climate App!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start_date<br/>"
        f"/api/v1.0/temp/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Returns json with the date as the key and the value as precipitation for the last year in the database
    start_date = dt.datetime(2016, 8, 22)
    end_date = dt.datetime(2017, 8, 23)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between(start_date, end_date)).all()
    precip = {date: prcp for date, prcp in prcp_scores}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset
    stations_query = session.query(Station.station)
    stations_list = [result.station for result in stations_query.all()]
    return jsonify({'station': stations_list})

@app.route("/api/v1.0/tobs")
def tobs():
    # Return a JSON list of temperature observations for the previous year for most active station
    start_date = dt.datetime(2016, 8, 22)
    end_date = dt.datetime(2017, 8, 23)
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between(start_date, end_date)).\
        filter(Measurement.station == 'USC00519281').all()
    tobs_list = {date: tobs for date, tobs in tobs_query}
    return jsonify(tobs_list)
    

@app.route("/api/v1.0/temp/<start_date>")
def calc_start_temp(start_date):
    # Added start_date as parameter. Function will return min, max, and avg temp for 
    # dates greater than or equal to given start_date
    try:
        # Convert the start_date string to a datetime object
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
        
        temp_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        
        # Extract results from the query
        min_temp, max_temp, avg_temp = temp_query[0]

        # Prepare response in JSON format
        response = {
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "avg_temperature": avg_temp
        }

        return jsonify(response)
    # Adding ValueError for invalid date format
    except ValueError:
        return "Invalid date format. Please provide a valid date string in the format YYYY-MM-DD."


@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def calc_temp_range(start_date, end_date):
    # Added start_date and end_date as parameter. Function will return min, max, and avg temp for 
    # dates between given start_date and end_date
    try:
        # Convert the start_date and end_date string to a datetime object
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
        
        temp_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

        # Extract results from the query
        min_temp, max_temp, avg_temp = temp_query[0]

        # Prepare response in JSON format
        response = {
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "avg_temperature": avg_temp
        }

        return jsonify(response)
    # # Adding ValueError for invalid date format
    except ValueError:
        return "Invalid date format. Please provide a valid date string in the format YYYY-MM-DD."


if __name__ == "__main__":
    app.run(debug=True)

session.close()