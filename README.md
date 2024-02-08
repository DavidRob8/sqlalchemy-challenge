# SQLAlchemy Challenge

In this module challenge we performed a climate analysis for Hawaii. 

In Part 1, I analyzed and explored the climate data using the climate_starter.ipynb file and the hawaii.sqlite database. I performed a precipitation analysis for the most recent year based off the most recent data in the dataset and plotted a barchat.
I then performed a station analysis by calculating the total number of stations and finding the most active id. I calculated the lowest, highest, and average temperatures by the most active station id.
Next, I created a histogram of the previous 12 months of temperature observations (TOBS).

In Part 2, I designed a climate app using Flask. I created a homepage that listed all available routes:

- Precipitation: returns the last 12 months of precipitation data
- Stations: returns the list of stations from the dataset
- TOBS - returns a list of temperature observations for the previous year
- Start Date: returns a list of min, max, and avg temperature from a specified start date
- Start Date/ End Date: returns a list of min, max, and avg temperature for a start-end range.

