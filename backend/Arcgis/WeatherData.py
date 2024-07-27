import pandas as pd
import requests
import os

apiKey = "edea8cd8a2ba480586e215247241107" # os.getenv("WEATHER_API_KEY")

df = pd.read_csv("data/2000-2024_fires.csv")

df_head = df.head()

# Create a dictionary to hold new column data
new_columns = {
    "condition": [],
    "temp_c": [],
    "wind_kph": [],
    "wind_dir": [],
    "precip_mm": [],
    "humidity": [],
}

for x in df_head.index:
    percentage = (x+1) / len(df_head) * 100
    print(f"{percentage}% done")
    lat = df_head.loc[x, "lat"]
    lon = df_head.loc[x, "lon"]
    df_head.loc[x, "date"] = "2012-05-12"
    dt = df_head.loc[x, "date"]
    

    url = f"http://api.weatherapi.com/v1/history.json?key={apiKey}&q={lat},{lon}&dt={dt}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)

        # Current weather data
        new_columns["condition"].append(data["current"]["condition"]["text"])
        new_columns["temp_c"].append(data["current"]["temp_c"])
        new_columns["wind_kph"].append(data["current"]["wind_kph"])
        new_columns["wind_dir"].append(data["current"]["wind_dir"])
        new_columns["precip_mm"].append(data["current"]["precip_mm"])
        new_columns["humidity"].append(data["current"]["humidity"])
    else:
        print("Error:", response.status_code, response.text)
        new_columns["condition"].append("")
        new_columns["temp_c"].append(0.0)
        new_columns["wind_kph"].append(0.0)
        new_columns["wind_dir"].append("")
        new_columns["precip_mm"].append(0.0)
        new_columns["humidity"].append(0)

weather_df = pd.DataFrame(new_columns, index=df.index)
df = pd.concat([df, weather_df], axis=1)
df.to_csv("Arcgis/data/2000-2024_fires+weather.csv", index=False)
print("done")