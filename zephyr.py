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
with open('synop.2022100706.csv') as input:
    weather_today = pd.read_csv(
        input,
        delimiter=';',
        dtype={'numer_sta': object}
    )

# open historic observation data for month
with open('synop.202209.csv') as input:
    weather_historical = pd.read_csv(
        input,
        delimiter=';',
        dtype={'numer_sta': object}
    )

# convert timestamp for historic data into datetime type
weather_historical['date'] = weather_historical['date'].apply(lambda x: pd.to_datetime(x, format="%Y%m%d%H%M%S"))

# Create map centred on Saulzais-le-Potier
map = folium.Map(location=[46.59878, 2.48712], zoom_start=6)

# Loop through stations in json
for station in observation_stations['features']:
    # Pull out the station data
    id = station['properties']['ID']
    name = station['properties']['Nom']
    latitude = station['properties']['Latitude']
    longitude = station['properties']['Longitude']
    # Select today's data
    station_today = weather_today.loc[weather_today['numer_sta'] == id].copy()
    wind = station_today['rafper'].to_string(index=False)
    # Select subset of historic data matching on id
    station_historic = weather_historical.loc[weather_historical['numer_sta'] == id, ['date', 'rafper']].copy()
    # Drop rows with no wind data
    station_historic_clean = station_historic[station_historic['rafper'] != "mq"].copy()
    # Check if dataframe is empty, if not construct chart
    if station_historic_clean.empty == False:
        # Convert historic wind data to float
        station_historic_clean['rafper'] = pd.to_numeric(station_historic_clean['rafper'])
        # Set chart title, wind stored as string so must convert
        if wind != "mq":
            chart_title = name + ': ' + wind + 'm/s'
        else:
            chart_title = name
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
        # Handle case where no wind data
        if wind != "mq":
            chart_with_rule = alt.layer(chart, yrule, data=station_historic_clean
            ).transform_calculate(
                a=wind
            )
        else:
            chart_with_rule = alt.layer(chart, yrule, data=station_historic_clean
            ).transform_calculate(
                a="0"
            )
        chart_json = chart_with_rule.to_json()
        popup = folium.Popup()
        folium.VegaLite(chart_json).add_to(popup)
    # Handle when dataframe is empty
    else:
        if wind != "mq":
            print(wind)
            popup_text = name + ': ' + wind[0] + 'm/s'
        else:
            popup_text = name
        popup = folium.Popup(
            html='<span style="display: inline; font-family:sans-serif; font-weight:bold; font-size:13px; color:#000; opacity:1">' + popup_text + '</span>'
            
        )
    custom_icon = folium.features.CustomIcon(
            'windsock.png',
            icon_size=(32,32)          
        )
    folium.Marker(
        location=[latitude, longitude],
        popup=popup,
        icon=custom_icon
    ).add_to(map)
map.save("index.html")
quit()

#folium.Icon(icon="cloud"),



#     chart = vincent.Scatter(hist_dict, iter_idx="x", width=600, height=300)
#     chart_json = chart.to_json()
#     #df = pd.DataFrame(list, columns=['date', 'wind'])



#     popup_example = folium.Popup(max_width=450)
#     folium.Vega(chart_json, height=350, width=650).add_to(popup_example)
#     #folium.Marker([30, -100], popup=popup).add_to(m)

    
#     folium.Marker(
#         location=[latitude, longitude],
#         label=name,
#         popup=popup_example,
#         icon=folium.Icon(icon="cloud"),
#     ).add_to(my_map)   

# my_map.save("index.html")



    

    #data_historic_chart = pd.DataFrame(data_historic_clean['rafper'], index=data_historic_clean['date'])
    #print(data_historic_clean)

    # Don't forget to check dataframe is empty






#     # Go through historical data
#     x_array = []
#     y_array = []
#     for i, row in df_historical BLAH BLAH OLD
#         id_historical = row['numer_sta']
#         if id_historical == id:
#             datetime_historical = row['date']
#             wind = row['rafper']
#             # Don't store if we have "mq" value
#             if wind == "mq":
#                 break
#             x_array.append(datetime_historical)
#             y_array.append(wind)
#     hist_dict.update({
#         "x": x_array,
#         "y": y_array
#     })
#     print(hist_dict)
#     
# 



#     # folium.Marker(
#     # location=[latitude, longitude],
#     #     popup=folium.Popup(max_width=450)
#     #         .add_child(
#     #             folium.Vega(example, width=450, height=250)
#     #         ),
#     #     icon=folium.Icon(icon="cloud"),
#     # ).add_to(my_map)   




# #     # Match the weather data
# #     weather_data = df.loc [df['numer_sta'] == id]
# #     # Wind columns: raf10 & rafper
# #     print(str(weather_data['raf10']))
# #     label = nom + " rafales: " + str(weather_data['rafper'].to_string(index=False)) + "m/s"
# #     folium.Marker(
# #         location=[latitude, longitude],
# #         popup=folium.Popup(max_width=450)
# #             .add_child(
# #                 folium.Vega(vega_test, width=450, height=250)
# #             ),
# #         icon=folium.Icon(icon="cloud"),
# #     ).add_to(my_map)

# #list_stations = []

# #df_historical.sort_values(by=['numer_sta'], inplace=True)

# # for i, row in df_historical.iterrows():
# #     id_historical = row['numer_sta']
# #     datetime_historical = row['date']
# #     wind = row['rafper']
# #     for station in observation_stations['features']:
# #         id = station['properties']['ID']
# #         if id == id_historical:
# #             nom = station['properties']['Nom']
# #             latitude = station['properties']['Latitude']
# #             longitude = station['properties']['Longitude']
# #             break
# #     data = {
# #         'numer_sta': id_historical,
# #         'nom': nom,
# #         'latitude': latitude,
# #         'longitude': longitude,
# #         'date': datetime_historical,
# #         'rafper': wind,
# #     }
# #     list_stations.append(data)

# # print(list_stations)





# #     id_historical = row['numer_sta']
# #     for station in observation_stations['features']:
# #         id = station['properties']['ID']
# #         nom = station['properties']['Nom']
# #         latitude = station['properties']['Latitude']
# #         longitude = station['properties']['Longitude']




