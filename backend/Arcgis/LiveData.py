from arcgis.gis import GIS
import requests
import json
import traceback
import pandas as pd
import os
from datetime import datetime
import pytz

apiKey = os.getenv("WEATHER_API_KEY")

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
    df = df.drop(['Agency', 'Fire_Name', 'ObjectId', 'GlobalID', 'Stage_of_Control', 'Time_Zone'], axis=1)
    df.rename(columns={'Hectares__Ha_': 'hectares'}, inplace=True)
    df.rename(columns={'Latitude': 'lat'}, inplace=True)
    df.rename(columns={'Longitude': 'lon'}, inplace=True)
    df['Start_Date'] = df['Start_Date'].astype(str)

    # format the time to datetime and timezone to utc
    for x in df.index:
        unixTime = int(df.loc[x, "Start_Date"])
        dtTime = convertDate(unixTime)
        df.loc[x, "Start_Date"] = dtTime

    df.rename(columns={'Start_Date': 'date'}, inplace=True)

    return df

def addWeatherData(df):

    # Specify the number of days for the forecast
    days = 3

    # Create a dictionary to hold new column data
    new_columns = {
        "condition": [],
        "temp_c": [],
        "wind_kph": [],
        "wind_dir": [],
        "precip_mm": [],
        "humidity": [],
    }

    # Add forecast columns for each day
    for i in range(1, days + 1):
        new_columns[f"condition_f{i}"] = []
        new_columns[f"maxtemp_c_f{i}"] = []
        new_columns[f"avgtemp_c_f{i}"] = []
        new_columns[f"maxwind_kph_f{i}"] = []
        new_columns[f"totalprecip_mm_f{i}"] = []
        new_columns[f"totalsnow_cm_f{i}"] = []
        new_columns[f"avghumidity_f{i}"] = []
        new_columns[f"daily_will_it_rain_f{i}"] = []
        new_columns[f"daily_will_it_snow_f{i}"] = []

    # For each row, add weather data
    for x in df.index:
        lat = df.loc[x, "lat"]
        lon = df.loc[x, "lon"]
        url = f"http://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={lat},{lon}&days={days}"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Current weather data
            new_columns["condition"].append(data["current"]["condition"]["text"])
            new_columns["temp_c"].append(data["current"]["temp_c"])
            new_columns["wind_kph"].append(data["current"]["wind_kph"])
            new_columns["wind_dir"].append(data["current"]["wind_dir"])
            new_columns["precip_mm"].append(data["current"]["precip_mm"])
            new_columns["humidity"].append(data["current"]["humidity"])

            # Forecast data
            for i in range(len(data["forecast"]["forecastday"])):
                rowData = data["forecast"]["forecastday"][i]["day"]
                new_columns[f"condition_f{i+1}"].append(rowData["condition"]["text"])
                new_columns[f"maxtemp_c_f{i+1}"].append(rowData["maxtemp_c"])
                new_columns[f"avgtemp_c_f{i+1}"].append(rowData["avgtemp_c"])
                new_columns[f"maxwind_kph_f{i+1}"].append(rowData["maxwind_kph"])
                new_columns[f"totalprecip_mm_f{i+1}"].append(rowData["totalprecip_mm"])
                new_columns[f"totalsnow_cm_f{i+1}"].append(rowData["totalsnow_cm"])
                new_columns[f"avghumidity_f{i+1}"].append(rowData["avghumidity"])
                new_columns[f"daily_will_it_rain_f{i+1}"].append(rowData["daily_will_it_rain"])
                new_columns[f"daily_will_it_snow_f{i+1}"].append(rowData["daily_will_it_snow"])
        else:
            print("Error:", response.status_code, response.text)
            new_columns["condition"].append("")
            new_columns["temp_c"].append(0.0)
            new_columns["wind_kph"].append(0.0)
            new_columns["wind_dir"].append("")
            new_columns["precip_mm"].append(0.0)
            new_columns["humidity"].append(0)

            for i in range(1, days + 1):
                new_columns[f"condition_f{i}"].append("")
                new_columns[f"maxtemp_c_f{i}"].append(0.0)
                new_columns[f"avgtemp_c_f{i}"].append(0.0)
                new_columns[f"maxwind_kph_f{i}"].append(0.0)
                new_columns[f"totalprecip_mm_f{i}"].append(0.0)
                new_columns[f"totalsnow_cm_f{i}"].append(0.0)
                new_columns[f"avghumidity_f{i}"].append(0.0)
                new_columns[f"daily_will_it_rain_f{i}"].append(0.0)
                new_columns[f"daily_will_it_snow_f{i}"].append(0.0)

        percentage = (x + 1) / len(df) * 100
        print(f"{percentage:.2f}% done")


    # Create a new DataFrame for the new columns
    weather_df = pd.DataFrame(new_columns, index=df.index)

    # Concatenate the original DataFrame with the new columns DataFrame
    df = pd.concat([df, weather_df], axis=1)

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
        existing_df = pd.read_csv("data/Active_Fires.csv")
        merged_df = pd.concat([df, existing_df], axis=0, ignore_index=True)
        dfLength = len(merged_df)
        merged_df = merged_df.drop_duplicates()
        newDfLength = len(merged_df)
        numDuplicates = dfLength - newDfLength
        print(f"Duplicates removed: {numDuplicates}")
        print(f"Null values removed: {numNa}")
        csv_file_path = os.path.join("data", "Active_Fires.csv")
        merged_df.to_csv(csv_file_path, index=False)  # Convert the pandas DataFrame to a csv
        print("Added data:")
        numNewData = currentLength - numDuplicates
        if (numNewData > 0):
            print(merged_df.tail(currentLength-numDuplicates))
        else:
            print("No data added")
        print("Done!")