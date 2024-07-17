from arcgis.gis import GIS
import traceback
import pandas as pd
import os
from datetime import datetime, timedelta

def getDataset(dataset_id):

    # Connect to ArcGIS Online
    gis = GIS("https://www.arcgis.com")

    # Get Active WildFires in Canada dataset
    wildfire_item = gis.content.get(dataset_id)

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

                # Convert the result to a pandas DataFrame
                return pd.DataFrame(query_result.features)
                
            except Exception as e:
                traceback.print_exc()
        else:
            print("No suitable layer found in the dataset")
    else:
        print("Unvalid dataset")

def cleanDataset(df):
    print(df.head())

if __name__ == "__main__":
    print("Retreaving the dataset...")
    df = getDataset("bf3aa167923a48929d23636c6e204c73")
    if df is not None:
        print("Succesfully retrieved the dataset")
        print("Cleaning the dataset...")
        cleanDataset(df)





# csv_file_path = os.path.join("data", f"{wildfire_title}.csv")
# df.to_csv(csv_file_path, index=False)