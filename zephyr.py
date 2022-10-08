import json
import folium
import pandas as pd

with open('postesSynop.json') as input:
    observation_stations = json.load(input)



with open('vega_test.json') as input:
    vega_test = json.load(input)

csv_file = 'synop.2022100706.csv'
csv_file_historical = 'synop.202209.csv'


# specify dtype as string for station ID
weather = pd.read_csv(
    csv_file,
    delimiter=';',
    dtype={'numer_sta': object}
    )
df = pd.DataFrame(weather)

weather_historical = pd.read_csv(
    csv_file_historical,
    delimiter=';',
    dtype={'numer_sta': object}
)
df_historical = pd.DataFrame(weather_historical)

# Convert into a proper datetime type
df_historical['date'] = df_historical['date'].apply(lambda x: pd.to_datetime(x, format="%Y%m%d%H%M%S"))

list_stations = []

df_historical.sort_values(by=['numer_sta'], inplace=True)

# for i, row in df_historical.iterrows():
#     id_historical = row['numer_sta']
#     datetime_historical = row['date']
#     wind = row['rafper']
#     for station in observation_stations['features']:
#         id = station['properties']['ID']
#         if id == id_historical:
#             nom = station['properties']['Nom']
#             latitude = station['properties']['Latitude']
#             longitude = station['properties']['Longitude']
#             break
#     data = {
#         'numer_sta': id_historical,
#         'nom': nom,
#         'latitude': latitude,
#         'longitude': longitude,
#         'date': datetime_historical,
#         'rafper': wind,
#     }
#     list_stations.append(data)

# print(list_stations)





#     id_historical = row['numer_sta']
#     for station in observation_stations['features']:
#         id = station['properties']['ID']
#         nom = station['properties']['Nom']
#         latitude = station['properties']['Latitude']
#         longitude = station['properties']['Longitude']






# # Create map
my_map = folium.Map(location=[47.117991, 1.685244], zoom_start=3)

# List for storing historical data
list = []

# Loop through stations in json
for station in observation_stations['features']:
    # Pull out the station data
    id = station['properties']['ID']
    nom = station['properties']['Nom']
    latitude = station['properties']['Latitude']
    longitude = station['properties']['Longitude']
    # Go through historical data
    for i, row in df_historical.iterrows():
        id_historical = row['numer_sta']
        if id_historical == id:
            datetime_historical = row['date']
            wind = row['rafper']
            # Don't store if we have "mq" value
            if wind == "mq":
                break
            data = {
                "date": datetime_historical,
                "wind": wind
            }
            list.append(data)
    df = pd.DataFrame(list, columns=['date', 'wind'])
    print(df)
    folium.Marker(
    location=[latitude, longitude],
    popup=folium.Popup(max_width=450)
        .add_child(
            folium.Vega(df, width=450, height=250)
        ),
        icon=folium.Icon(icon="cloud"),
    ).add_to(my_map)   

my_map.save("index.html")




#     # Match the weather data
#     weather_data = df.loc [df['numer_sta'] == id]
#     # Wind columns: raf10 & rafper
#     print(str(weather_data['raf10']))
#     label = nom + " rafales: " + str(weather_data['rafper'].to_string(index=False)) + "m/s"
#     folium.Marker(
#         location=[latitude, longitude],
#         popup=folium.Popup(max_width=450)
#             .add_child(
#                 folium.Vega(vega_test, width=450, height=250)
#             ),
#         icon=folium.Icon(icon="cloud"),
#     ).add_to(my_map)




