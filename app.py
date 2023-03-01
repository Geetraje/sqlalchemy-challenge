import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd


#Setting up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


#Reflect an existing database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(autoload_with=engine)

#Saving reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Setting up Flask
app = Flask(__name__)


#Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>" )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

 #Query  
    date = dt.datetime(2016,8,23)
    one_year_prcp = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date > date).\
                    order_by(Measurement.date).all()
    
    session.close()

 #Create a dictionary
    precipitation = []
    for date, prcp in one_year_prcp:
        precipitation_dict = {date:prcp}
        precipitation.append(precipitation_dict)   
    return jsonify(precipitation)
   
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)    

    #Query the list of station names
    results = session.query(Station.station).all()
    
    session.close()
    all_names = list(np.ravel(results))
    
    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)                     
                    
    #Query    
    query_date = dt.date(2017,8,23)- dt.timedelta(days=365)
    one_year_temp = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= query_date).\
                    filter(Measurement.station == 'USC00519281').\
                    order_by(Measurement.date).all()

    session.close()

    #Create a dictionary
    temperature = []
    for date, tobs in one_year_temp:
        temperature_dict = {date:tobs}
        temperature.append(temperature_dict)   
    return jsonify(temperature)


@app.route("/api/v1.0/<start>")
def():
    #start_date = request.args.get('start')
     
    # Create session (link) from Python to the DB
    session = Session(engine)  

   
    
    sel = [Measurement.station,func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]
    start_date = dt.date(2015,5,10)    
    result = session.query(*sel).\
             filter(Measurement.date >= start_date).\
             group_by(Measurement.station).all()

    session.close()
    
    df= pd.DataFrame(result,columns=['STATION','TMIN','TAVG','TMAX'])
    analyse = df.values.tolist()
    analyse_dict = df.to_dict()
   
        
    return jsonify(analyse)

if __name__ == '__main__':
    app.run(debug=True)










    
    
    
    
    
    
    
    
    
    
    