import openmeteo_requests
import pandas as pd
import numpy as np
import requests
import os
import time

df = pd.read_csv("data/2000-2021_nofires.csv")
INSTANCE = 2
df = np.array_split(df, 6)[INSTANCE]
start_index = df.index[0]

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
    
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date,
        "end_date": date,
        "hourly": ["relative_humidity_2m", "surface_pressure", "soil_temperature_0_to_7cm", "soil_moisture_0_to_7cm"],
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
    
    index = x - start_index
    df_rows = df.iloc[:index+1]
    new_columns_df = pd.DataFrame(new_columns, index=df_rows.index)
    combined_df = pd.concat([df_rows, new_columns_df], axis=1)
    combined_df.to_csv("data/2000-2021_nofires+weather.csv", index=False)

    percentage = (index + 1) / len(df) * 100
    print(f"Instance: {INSTANCE}, {percentage:.3f}% done")
    time.sleep(9)

weather_df = pd.DataFrame(new_columns, index=df.index)
df = pd.concat([df, weather_df], axis=1)
df.to_csv("data/2000-2021_nofires+weather.csv", index=False)
print("done")