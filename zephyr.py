import json
import folium
import pandas as pd
import numpy as np
import altair as alt
import folium.features

# open json of observations stations
with open('postesSynop.json') as input:
    observation_stations = json.load(input)

# open latest observation data from today
with open('synop.2022102512.csv') as input:
    weather_today = pd.read_csv(
        input,
        delimiter=';',
        header=0,
        dtype={'numer_sta': object}
    )

# open historic observation data for same month last year
with open('synop.202110.csv') as input:
    weather_historic = pd.read_csv(
        input,
        delimiter=';',
        dtype={'numer_sta': object}
    )

# convert timestamp for historic data into datetime type
weather_historic['date'] = weather_historic['date'].apply(lambda x: pd.to_datetime(x, format="%Y%m%d%H%M%S"))

# convert wind to float
weather_today['rafper'] = weather_today['rafper'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
weather_historic['rafper'] = weather_historic['rafper'].apply(lambda x: pd.to_numeric(x, errors='coerce'))

# Create map centred on Saulzais-le-Potier, middle of France
map = folium.Map(location=[46.59878, 2.48712], zoom_start=6)

# Loop through stations in json
for station in observation_stations['features']:
    # Pull out the station data
    id = station['properties']['ID']
    name = station['properties']['Nom']
    latitude = station['properties']['Latitude']
    longitude = station['properties']['Longitude']
    # Select today's data
    station_today = weather_today[weather_today['numer_sta'] == id]['rafper']
    # Escape empty dataframe
    if station_today.empty:
        continue
    # Select today's wind speed
    wind = station_today.iloc[0]
    # Select subset of historic data matching on id
    station_historic = weather_historic.loc[weather_historic['numer_sta'] == id, ['date', 'rafper']]
    # Drop rows with no wind data
    station_historic_wind = station_historic.dropna(subset=['rafper'])
    #Escape empty dataframe
    if station_historic_wind.empty:
        continue
    # Set chart title, including today's wind speed
    chart_title = name + ': ' + str(wind) + 'm/s'
    # Create chart
    chart = alt.Chart(height=300, width=400).mark_line(interpolate='step-after').encode(
        alt.X('date:T', title="date/time"),
        alt.Y('rafper:Q', title="wind speed (m/s)")
    ).properties(
        title= chart_title
    )
    # Create a horizontal rule marking today's wind speed
    yrule = alt.Chart().mark_rule(color='red').encode(
        y='a:Q'
    )
    # Put chart and horizontal rule into a layer
    chart_with_rule = alt.layer(chart, yrule, data=station_historic_wind
    ).transform_calculate(
        a=str(wind)
    )
    # Convert to json and add chart layer to popup
    chart_json = chart_with_rule.to_json()
    popup = folium.Popup()
    folium.VegaLite(chart_json).add_to(popup)
    # Set icon for marker
    custom_icon = folium.features.CustomIcon(
        'windsock.png',
        icon_size=(32,32)          
    )
    # Add marker to map
    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=custom_icon
    ).add_to(map)
map.save("wind_map_france.html")
quit()