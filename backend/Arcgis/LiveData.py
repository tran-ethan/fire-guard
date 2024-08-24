from arcgis.gis import GIS
import openmeteo_requests
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import json
import traceback
import pandas as pd
import os
from datetime import datetime
import pytz
import time

canada_boundaries = gpd.read_file('data/canada_boundary.geojson')
HOUR = 3600
retrying = False

timezoneDict = {
    'MDT': 'America/Denver', # UTC-6
    'MST': 'America/Los_Angeles', # UTC-7
    'PDT': 'America/Los_Angeles', # UTC-7
    'PST': 'America/Vancouver', # JTC-8
    'EDT': 'America/New_York', # UTC-4
    'EST': 'America/Chicago', # UTC-5
    'CDT': 'America/Chicago', # UTC-5
    'CST': 'America/Guatemala', # UTC-6
    'GMT': 'Etc/GMT', # UTC+0
    'ADT': 'America/Halifax', # UTC-3
    'AST': 'America/Montreal' # UTC-4
}

def getDataset():

    # Connect to ArcGIS Online
    gis = GIS("https://www.arcgis.com")

    # Get Active WildFires in Canada dataset
    searchRes = gis.content.search(query="Active Wildfires in Canada", item_type="Feature Layer", max_items=10)
    wildfire_item = None

    for item in searchRes:
        if (item.title == "Active Wildfires in Canada"):
            wildfire_item = item
            break

    if (wildfire_item):

        wildfire_layer = None

        try:
            wildfire_layer = wildfire_item.layers[0]  # Access the first layer
        except:
            print("No layers found in the dataset")

        if (wildfire_layer):

            fields = wildfire_layer.properties.fields

            # Gets the date property in the dataset

            date_field = None
            for field in fields:
                if field.type == "esriFieldTypeDate":
                    date_field = field.name
                    break

            todayStart = datetime.now().strftime("%Y-%m-%d 00:00:00")  
            todayEnd = datetime.now().strftime("%Y-%m-%d 23:59:59")
            
            # Specify the time interval
            where_clause = f"{date_field} >= DATE '{todayStart}' AND {date_field} <= DATE '{todayEnd}'"

            # Query the feature layer for live data
            try :
                query_result = wildfire_layer.query(where=where_clause, out_fields="*", result_record_count=1000)

                if query_result.features:
                    # Convert the result to a pandas DataFrame
                    df = pd.DataFrame(query_result.features)
                    csv_file_path = os.path.join("data", "rawData.csv")
                    df.to_csv(csv_file_path, index=False)  # Convert the pandas DataFrame to a csv
                    print("Sucessfully retrieved the dataset")
                    retrying = False
                    return df
                else:
                    print("The result of the query is empty, retrying in one hour")
                    retrying = True
                    return None
            except Exception as e:
                traceback.print_exc()
        else:
            print("No suitable layer found in the dataset")
    else:
        print("Unvalid dataset")

def cleanDataset(data):

    cleanedDict = {
        "features" : []
    }

    for i in range(len(data)):
        row = data[i]['0']
        parsedRow = json.loads(row)   
        cleanedDict["features"].append(parsedRow["attributes"])

    attributesData = [cleanedDict["features"][i] for i in range(len(cleanedDict['features']))]

    df = pd.DataFrame(attributesData)
    df = df.drop(['Agency', 'Fire_Name', 'ObjectId', 'GlobalID', 'Stage_of_Control', "Time_Zone"], axis=1)
    df.rename(columns={'Hectares__Ha_': 'hectares'}, inplace=True)
    df.rename(columns={'Latitude': 'lat'}, inplace=True)
    df.rename(columns={'Longitude': 'lon'}, inplace=True)
    df['Start_Date'] = df['Start_Date'].astype(str)

    len_df = len(df)
    indicesToDrop = []

    # format the time to datetime and timezone to utc and check if points are inside Canada
    for x in df.index:
        lat = df.loc[x, "lat"]
        lon = df.loc[x, "lon"]
        if (not isWithinCanada(lat,lon)):
            indicesToDrop.append(x)
        else:
            unixTime = int(df.loc[x, "Start_Date"])
            dtTime = convertDate(unixTime)
            df.loc[x, "Start_Date"] = dtTime
    
    df = df.drop(indicesToDrop)
    len_cleaned_df = len(df)
    rows_not_Canada = len_df - len_cleaned_df

    print(f"Rows not in Canada removed: {rows_not_Canada}")

    df.rename(columns={'Start_Date': 'date'}, inplace=True)

    return df

def addWeatherData(df):

    # Create a dictionary to hold new column data
    new_columns = {
        "elevation": [],
        "temp_c": [],
        "max_temp_c": [],
        "min_temp_c": [],
        "wind_kph": [],
        "wind_dir": [],
        "precip_mm": [],
        "humidity": [],
        "pressure_hPa": [],
        "soil_temp_c": [],
        "soil_moisture": [],
        "totalsnow_cm": []
    }

    # Setup the Open-Meteo API client
    openmeteo = openmeteo_requests.Client()

    for x in df.index:

        lat = df.loc[x, "lat"]
        lon = df.loc[x, "lon"]
        date = df.loc[x, "date"]
        
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": date,
            "end_date": date,
            "hourly": ["relative_humidity_2m", "surface_pressure", "soil_temperature_0cm", "soil_moisture_0_to_1cm"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "rain_sum", "snowfall_sum", "wind_speed_10m_max", "wind_direction_10m_dominant"]
        }

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Check if the request was successful
        if (response):

            hourly = response.Hourly()
            humidity = round(np.mean(hourly.Variables(0).ValuesAsNumpy()), 3)
            pressure_hPa = round(np.mean(hourly.Variables(1).ValuesAsNumpy()), 3)
            soil_temp_c = round(np.mean(hourly.Variables(2).ValuesAsNumpy()), 3)
            soil_moisture = round(np.mean(hourly.Variables(3).ValuesAsNumpy()), 3)

            daily = response.Daily()
            max_temp_c = round(daily.Variables(0).ValuesAsNumpy()[0], 3)
            min_temp_c = round(daily.Variables(1).ValuesAsNumpy()[0], 3)
            temp_c = round(daily.Variables(2).ValuesAsNumpy()[0], 3)
            precip_mm = round(daily.Variables(3).ValuesAsNumpy()[0], 3)
            totalsnow_cm = round(daily.Variables(4).ValuesAsNumpy()[0], 3)
            wind_kph = round(daily.Variables(5).ValuesAsNumpy()[0], 3)
            wind_dir = round(daily.Variables(6).ValuesAsNumpy()[0], 3)

            new_columns["elevation"].append(response.Elevation())
            new_columns["temp_c"].append(temp_c)
            new_columns["max_temp_c"].append(max_temp_c)
            new_columns["min_temp_c"].append(min_temp_c)
            new_columns["wind_kph"].append(wind_kph)
            new_columns["wind_dir"].append(wind_dir)
            new_columns["precip_mm"].append(precip_mm)
            new_columns["humidity"].append(humidity)
            new_columns["pressure_hPa"].append(pressure_hPa)
            new_columns["soil_temp_c"].append(soil_temp_c)
            new_columns["soil_moisture"].append(soil_moisture)
            new_columns["totalsnow_cm"].append(totalsnow_cm)
        else:

            print("Error calling the API")

            new_columns["elevation"].append(0.0)
            new_columns["temp_c"].append(0.0)
            new_columns["max_temp_c"].append(0.0)
            new_columns["min_temp_c"].append(0.0)
            new_columns["wind_kph"].append(0.0)
            new_columns["wind_dir"].append(0.0)
            new_columns["precip_mm"].append(0.0)
            new_columns["humidity"].append(0.0)
            new_columns["pressure_hPa"].append(0.0)
            new_columns["soil_temp_c"].append(0.0)
            new_columns["soil_moisture"].append(0.0)
            new_columns["totalsnow_cm"].append(0.0)

        percentage = (x + 1) / len(df) * 100
        print(f"{percentage:.2f}% done")

    # Create a new DataFrame for the new columns
    weather_df = pd.DataFrame(new_columns, index=df.index)

    # Concatenate the original DataFrame with the new columns DataFrame
    df = pd.concat([df, weather_df], axis=1)

    return df

def convertDate(time):
    timeSeconds = time / 1000.0
    dtObj = datetime.fromtimestamp(timeSeconds)
    return dtObj.strftime('%Y-%m-%d')

def convertTimezone(timezone, time):
    timezoneName = pytz.timezone(timezoneDict[timezone])
    timeFormat = "%Y-%m-%d"
    dtObj = datetime.strptime(time, timeFormat)
    localTime = timezoneName.localize(dtObj)
    utcTime = localTime.astimezone(pytz.utc).strftime(timeFormat)
    return utcTime

def isWithinCanada(lat, lon):
    point = Point(lon, lat)
    return canada_boundaries.contains(point).any()

if __name__ == "__main__":

    print("Retrieving the dataset...")

    for i in range(3):
        res = getDataset()
        if (not retrying): break

    if (res is not None):

        # Getting the dataset
        df = pd.read_csv("data/rawData.csv")
        print(str(len(df)) + " rows of data found", end="\n\n")
        jsonData = df.to_json(orient='records')
        dictData = json.loads(jsonData)

        # Cleaning the dataset
        print("Cleaning the data...")
        df = cleanDataset(dictData)
        print("Cleaning done", end="\n\n")

        # Adding weather data
        print("Adding weather data...")
        df = addWeatherData(df)
        lenNa = len(df)
        df = df.dropna(how='any')
        currentLength = len(df)
        numNa = lenNa - currentLength
        print()

        # Writing df as csv
        print("Writing df as csv...")
        os.remove("data/rawData.csv")

        # Retrieve the old df and merge it with the new one

        save_path = "data/Active_Fires.csv"
        existing_df = pd.read_csv("data/Active_Fires.csv")
        dfLength = len(df)
        df = df.drop_duplicates(subset=['lat', 'lon', 'date'])
        newDfLength = len(df)
        numDuplicates = dfLength - newDfLength
        merged_df = pd.concat([df, existing_df], axis=0, ignore_index=True)
        merged_df.to_csv(save_path, index=False)
        print(f"Duplicates removed: {numDuplicates}")
        print(f"Null values removed: {numNa}")
        print("Added data:")
        if (newDfLength > 0):
            print(df)
        else:
            print("No data added")
        print("Done!")