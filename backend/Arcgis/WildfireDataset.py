from arcgis.gis import GIS
import requests
import json
import traceback
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz

apiKey = "edea8cd8a2ba480586e215247241107"

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
        # wildfire_item = gis.content.get(dataset_id)
    searchRes= gis.content.search(query="Active Wildfires in Canada", item_type="Feature Layer", max_items=10)
    wildfire_item = None


    for item in searchRes:
        if (item.title == "Active Wildfires in Canada"):
            wildfire_item = item
            break

    if (wildfire_item):
        wildfire_title = wildfire_item.title

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
                    csv_file_path = os.path.join("data", f"{wildfire_title}.csv")
                    df.to_csv(csv_file_path, index=False)  # Convert the pandas DataFrame to a csv
                    return df
                    print("Sucessfully downloaded the dataset")
                else:
                    print("The result of the query is empty")
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
    df = df.drop(['Agency', 'Fire_Name', 'ObjectId', 'GlobalID'], axis=1)
    df.rename(columns={'Hectares__Ha_': 'Hectares'}, inplace=True)
    df.rename(columns={'Stage_of_Control': 'Stage of Control'}, inplace=True)
    df['Start_Date'] = df['Start_Date'].astype(str)

    # format the time to datetime and timezone to utc
    for x in df.index:
        unixTime = int(df.loc[x, "Start_Date"])
        timezone = df.loc[x, "Time_Zone"]
        dtTime = convertDate(unixTime)
        utcTime = convertTimezone(timezone, dtTime)
        df.loc[x, "Start_Date"] = utcTime

    df = df.drop(['Time_Zone'], axis=1)
    df.rename(columns={'Start_Date': 'Start Date (UTC)'}, inplace=True)

    return df

def addWeatherData(df):

    # Create new columns

    df["Temperature (°C)"] = 0.0
    df["Wind speed (kph)"] = 0.0
    df["Wind direction"] = ""
    df["Precipitation (mm)"] = 0.0
    df["humidity"] = 0

    # For each row, add weather data

    for x in df.index:
        lat = df.loc[x, "Latitude"]
        long = df.loc[x, "Longitude"]
        url = f"http://api.weatherapi.com/v1/current.json?key={apiKey}&q={lat},{long}"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            temp_c = data["current"]["temp_c"]
            wind_kph = data["current"]["wind_kph"]
            wind_dir = data["current"]["wind_dir"]
            precip_mm = data["current"]["precip_mm"]
            humidity =  data["current"]["humidity"]

            df.loc[x, "Temperature (°C)"] = temp_c
            df.loc[x, "Wind speed (kph)"] = wind_kph
            df.loc[x, "Wind direction"] = wind_dir
            df.loc[x, "Precipitation (mm)"] = precip_mm
            df.loc[x, "humidity"] = humidity
        else:
            print("Error:", response.status_code, response.text)

    return df

def convertDate(time):

    timeSeconds = time / 1000.0
    dtObj = datetime.utcfromtimestamp(timeSeconds)
    return dtObj.strftime('%Y-%m-%d %H:%M:%S')

def convertTimezone(timezone, time):
    timezoneName = pytz.timezone(timezoneDict[timezone])

    timeFormat = "%Y-%m-%d %H:%M:%S"

    dtObj = datetime.strptime(time, timeFormat)

    localTime = timezoneName.localize(dtObj)

    utcTime = localTime.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')

    return utcTime

if __name__ == "__main__":

    print("Retrieving the dataset...")
    res = getDataset()

    if (res is not None):

        df = pd.read_csv("data/Active Wildfires in Canada.csv")
        jsonData = df.to_json(orient='records')
        dictData = json.loads(jsonData)

        print("Cleaning the data")
        df = cleanDataset(dictData)
        print("cleaning done")

        print("Adding weather data...")
        df = addWeatherData(df)

        print("Writing df as csv...")
        os.remove("data/Active Wildfires in Canada.csv")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        csv_file_path = os.path.join("data", f"Active Wildfires in Canada ({current_time}).csv")
        df.to_csv(csv_file_path, index=False)  # Convert the pandas DataFrame to a csv
        print("Done!")