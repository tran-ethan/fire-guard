import pandas as pd
import numpy as np
import requests
import time

url = "http://geogratis.gc.ca/services/elevation/cdem/altitude?"
def get_altitude(lat: float, lon: float):
  response = requests.get(f"{url}lat={lat}&lon={lon}")

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      try:
            # Parse the response JSON
            data = response.json()
            # Extract the altitude value (assuming the key is 'altitude')
            altitude = data.get('altitude')
            if altitude is not None:
                return altitude
            else:
                print('Altitude data not found in response')
      except ValueError:
            print('Failed to parse JSON response')
  else:
      print('Failed to get altitude')

  return None

def add_altitude_column(df: pd.DataFrame, header: bool = False):
    """
    Add altitude column to the dataframe using get_altitude function. Save the updated dataframe to a csv file.

    Args:
        df (pd.DataFrame): The dataframe to add the altitude column to
        header (bool): Whether to write the header to the csv file. Default is False

    Returns:
        None
    """

    df['altitude'] = df.apply(lambda row: get_altitude(row['lat'], row['lon']), axis=1)
    df.to_csv("1950-2021_fires_with_altitude.csv", mode='a', index=False, header=header)

def add_elevation(dfs: list[pd.DataFrame], start_index: int, batch_limit: int, wait_minutes: int):
    """
    Add elevation to the dataframes in the list using canada elevation API.

    Args:
        dfs (list[pd.DataFrame]): The list of dataframes to add elevation to
        start_index (int): The index to start from
        batch_limit (int): The number of batches to do before waiting
        wait_minutes (int): The number of minutes to wait after every batch_limit batches

    Returns:
        None
    """
    if start_index == 0:
        print("Adding altitude to the dataset...")
        print("Adding altitude to batch 1...")
        add_altitude_column(dfs[0], header=True)
        print("Batch 1 complete")
        start_index += 1

    for df in dfs[start_index:]:
        if start_index % batch_limit == 0:
            print(f"{batch_limit} batches complete.")
            print(f"Waiting for {wait_minutes} minutes in order to avoid rate limiting...")
            time.sleep(wait_minutes * 60)
        
        print(f"Adding altitude to batch {start_index}...")
        add_altitude_column(df)
        print(f"Batch {start_index} complete\n")
        start_index += 1

# Load the data
dataset = pd.read_csv("1950-2021_fires.csv")
#Split the df into len(dataset) // 1000 batches
dfs = np.array_split(dataset, len(dataset) // 1000)
# Add elevation to the dataframes
add_elevation(dfs, 13, 10, 20)