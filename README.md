# FireGuard 

Interactive web-based map displaying wildfire predictions using machine learning model trained on historical climate data

https://github.com/user-attachments/assets/f4e8151f-29d9-4243-af61-77d0fcf13078

- [Full Project Presentation](https://youtu.be/jtjfIgHGFrI?si=_yAGnr6Y3Fs3ZftO)
- [Detailed project outline](./docs/Project_Blueprint.pdf)

## Problem
Wildfires pose a significant threat to both human life and property. The inability to accurately forecast when and where wildfires will occur leads to insufficient time for evacuation and preparation, increasing the risk of loss of life and property.

By accurately predicting wildfires locations, we can:
- Enhance public safety and preparedness
- Reduce loss of life and property damage
- Improve resource allocation for firefighting and emergency response teams

Our solution involved the development of a Random Forests classification machine learning model using sci-kit learn trained on historical wildfire data which predicts the likelihood and location of future wildfires using current geographic and climate data.

## Datasets
Data sources
- Environment and Climate Change Canada's [MSC GeoMet Dataset](https://api.weather.gc.ca/collections?lang=en)
- [ArcGIS](https://www.arcgis.com/index.html)
- [Kaggle Wildfires in Canada (1950-2021) dataset](https://www.kaggle.com/datasets/ulasozdemir/wildfires-in-canada-19502021/code)
Data collection
- ArcGIS
- [Open-Meteo](https://open-meteo.com/)
Data attributes
- Metorological data (max/min/mean temperature, wind speed/direction, precipitation, humidity, pressure, soil temperature/moisture, date) along with coordinates (lat/lon) to train the model
- Used servers with python scripts to clean data, and add weather data to a larger data set