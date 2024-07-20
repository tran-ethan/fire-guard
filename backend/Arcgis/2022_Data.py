from arcgis.gis import GIS
from arcgis.geometry import Geometry, SpatialReference, project
import json
import traceback
import pandas as pd
import os
from datetime import datetime, timedelta
import time

gis = GIS("https://www.arcgis.com")


def getDataset():

    # Connect to ArcGIS Online
    # gis = GIS("https://www.arcgis.com")

    # Get Active WildFires in Canada dataset
    searchRes= gis.content.search(query="Wildfires Canada 2022", item_type="Feature Layer", max_items=10)
    wildfire_item = None

    for item in searchRes:
        print(f"Title: {item.title}, ID: {item.id}")

    input_id = input("Enter the ID to choose data: ")

    wildfire_item = None
    wildfire_title = None
    for item in searchRes:
        if item.id == input_id:
            wildfire_item = item
            wildfire_title = item.title
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

            start_date = "2022-01-01 00:00:00"
            end_date = "2022-12-31 23:59:59"
            
            # Specify the time interval
            where_clause = f"{date_field} >= DATE '{start_date}' AND {date_field} <= DATE '{end_date}'"

            # Query the feature layer for live data
            try :
                query_result = wildfire_layer.query(where=where_clause, out_fields="*", result_record_count=1000)

                if query_result.features:
                    # Convert the result to a pandas DataFrame
                    df = pd.DataFrame(query_result.features)
                    csv_file_path = os.path.join("data", "2022_fires.csv")
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
        "features": []
    }

    for i in range(len(data)):
        row = data[i]['0']
        parsedRow = json.loads(row)

        spatial_ref = parsedRow["geometry"]["spatialReference"]
        attributes = parsedRow["attributes"]
        ringDict = {}
        ringDict["ringX"] = parsedRow["geometry"]["rings"][0][0][0]
        ringDict["ringY"] = parsedRow["geometry"]["rings"][0][0][1]

        # Merge spatialReference and attributes into a single dictionary
        merged_dict = {**ringDict, **spatial_ref, **attributes}
        cleanedDict["features"].append(merged_dict)

    # Create DataFrame from features list
    df = pd.DataFrame(cleanedDict["features"])

    columns_to_drop = ['OBJECTID', 'YEAR', 'NFIREID', 'BASRC', 'FIREMAPS', 'FIREMAPM', 'FIRECAUS',
                    'BURNCLAS', 'EDATE', 'AFSDATE', 'AFEDATE', 'CAPDATE', 'ADJ_HA', 'ADJ_FLAG',
                    'AGENCY', 'BT_GID', 'VERSION', 'COMMENTS', 'AFSDATE_MODIFIED', 'Shape__Area',
                    'Shape__Length']
                    
    df = df.drop(columns_to_drop, axis=1)

    df["lat"] = 0.0
    df["lon"] = 0.0
    df['SDATE'] = df['SDATE'].astype(str)

    for i in df.index:
        x = df.loc[i, "ringX"]
        y = df.loc[i, "ringY"]
        wkid = df.loc[i, "wkid"]
        latestWkid = df.loc[i, "latestWkid"]
        lat, lon = calculateCoords(x, y, wkid, latestWkid)
        df.loc[i, "lat"] = lat
        df.loc[i, "lon"] = lon

        unixTime = int(df.loc[i, "SDATE"])
        dtTime = convertDate(unixTime)
        df.loc[i, "SDATE"] = dtTime

    df = df.drop(['ringX', 'ringY', 'wkid', 'latestWkid'], axis=1)
    lat_col = df.pop('lat')
    lon_col = df.pop('lon')
    df.insert(0, 'lat', lat_col)
    df.insert(1, 'lon', lon_col)

    df.rename(columns={'SDATE': 'date'}, inplace=True)
    df.rename(columns={'POLY_HA': 'hectares'}, inplace=True)

    return df

def calculateCoords(x, y, wkid, latestWkid):

    input_sr = SpatialReference(wkid=wkid)

    # Create a Geometry object with the point
    point = Geometry({
        "x": x,
        "y": y,
        "spatialReference": input_sr
    })

    # Define the target spatial reference (WGS84)
    target_sr = SpatialReference(wkid=4326)

    # Use the project function to convert the point to geographic coordinates
    projected_point = project([point], input_sr, target_sr)

    # Check if the projection was successful
    if projected_point:
        # Extract the longitude and latitude from the projected_point
        projected_geometry = projected_point[0]
        longitude = projected_geometry["x"]
        latitude = projected_geometry["y"]

        return [latitude, longitude]
    else:
        print("Projection failed. The result is None.")

def convertDate(time):

    timeSeconds = time / 1000.0
    dtObj = datetime.utcfromtimestamp(timeSeconds)
    return dtObj.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # getDataset()

    start_time = time.time()

    df = pd.read_csv("data/2022_fires.csv")
    jsonData = df.to_json(orient='records')
    dictData = json.loads(jsonData)

    print("Cleaning data...")
    df = cleanDataset(dictData)

    end_time = time.time()

    print("Writing df as csv...")
    csv_file_path = os.path.join("data", "2022_fires(2).csv")
    df.to_csv(csv_file_path, index=False)  # Convert the pandas DataFrame to a csv
    print("Done!")

    delta_t = end_time - start_time
    print(f"Elapsed Time: {delta_t}")