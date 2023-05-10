# sqlalchemy-challenge
SQLAlchemy Challenge

Part 1: Analyse and Explore the Climate Data
Using Python (Pandas and Matplotlib) and SQLAlchemy (ORM Queries) to do a basic climate analysis and data exploration Hawaii climate database (measurement.csv and station.csv).

For Precipiation Analysis
- Find most recent data in the dataset
- Using the date above, get the previous 12 months of precipitation data by querying the previous 12 months of data.
- Select on data and precipitation values, and load as dataframe, sort by date
- Plot the results
- Perform summary statistics for the precipitation data

For Station Analysis
- Design a query to calculate the total number of stations in the dataset.
- Design a query to list stations and observation counr in descending order
- Select the station with the highest number of observation
- Using that station to calculate the lowest, highest and average temperatures
- Design a query to get the previous 12 months of temperature observation (TOBS) data, filter by station with highst number of observation
- Plot the histogram

Part 2: Design the Climate app
Using Flask API, use Flask to create a climate app for the following:
- Homepage to list all available paths
- Precipitation Path
- Station Path
- TOBS Path
- Start Date Path to calculate Min, Max, Avg temperature for a specific date
- Start to End Date path to calculate Min, Max, Avg temperature for a specific date range