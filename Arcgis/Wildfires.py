from arcgis.gis import GIS
import pandas as pd
import os

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com")

# Search for Wildfire Data in Canada
search_result = gis.content.search("Wildfire Canada", item_type="Feature Layer")

if len(search_result) > 0:
    for item in search_result:
        print(f"Title: {item.title}, ID: {item.id}")

    print()
    wildfire_id = input("Enter the id of a wildfire: ") 
    wildfire_item = None
    wildfire_title = None

    for item in search_result:
        if item.id == wildfire_id:
            wildfire_item = item
            wildfire_title = item.title
            break

    wildfire_layer = None

    try:
        wildfire_layer = wildfire_item.layers[0]  # Access the first layer
    except:
        print("Enter a valid id")

    if (wildfire_layer):

        # Query the feature layer for live data (example: query top 10 records)
        query_result = wildfire_layer.query(where="1=1", out_fields="*", result_record_count=10)
        
        # Convert the result to a pandas DataFrame
        df = pd.DataFrame(query_result.features)
        
        csv_file_path = os.path.join("data", f"{wildfire_title}.csv")
        df.to_csv(csv_file_path, index=False)  # Convert the pandas DataFrame to a csv
    else:
        print("No suitable wildfire data found.")
