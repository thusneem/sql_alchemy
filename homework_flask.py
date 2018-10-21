import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
        f"Welcome to Climate App <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all """
    percipitation_data = session.query(Measurement.date,Measurement.prcp).\
                        filter(Measurement.date <= '2017-08-23').\
                        filter( Measurement.date >= '2016-08-23').\
                        filter(Measurement.prcp != 'None').all()
    all_percp=[]
    for percipitation in percipitation_data:
        percp_dict ={}
        percp_dict["dates"] =percipitation.date
        percp_dict["prcp"] =percipitation.prcp
        all_percp.append(percp_dict) 
    return jsonify(all_percp)


@app.route("/api/v1.0/stations")
def stations():
    active_stations =session.query(Measurement.station,func.count(Measurement.station)).\
                              group_by(Measurement.station).\
                              order_by(func.count(Measurement.station).desc()).all()
    all_stations = list(np.ravel(active_stations))
    return jsonify(all_stations)
        

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all tobs
    temp_obs_lastyear=session.query(Measurement.date,Measurement.tobs).\
                     filter( Measurement.date <= '2017-08-23').\
                     filter( Measurement.date >= '2016-08-23').\
                     filter(Measurement.station == 'USC00519281').all()
  # Create a list 
    all_tobs = list(np.ravel(temp_obs_lastyear))
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/start/end")
def start_end():
    func_prv_year= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >='2017-02-28').\
            filter(Measurement.date <= '2017-03-05').all()
    
    all_trip = list(np.ravel(func_prv_year))
    return jsonify(all_trip)

if __name__ == '__main__':
    app.run(debug=True)
