from datetime import datetime
import os
import pandas as pd

from django.contrib import admin
from geoQuakesapp.models import Quake

admin.site.register(Quake)

# Check whether the table is empty before adding the dataset
if Quake.objects.all().count() == 0:
    # https://github.com/EBISYS/WaterWatch
    water_watch_data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, 'static', 'resources', 'database.csv'))
    df = pd.read_csv(water_watch_data_path)
    drop_cols = [
        'Time', 'Depth Seismic Stations', 'Magnitude Error', 'Magnitude Seismic Stations', 'Azimuthal Gap',
        'Horizontal Distance', 'Horizontal Error', 'Root Mean Square', 'Source', 'Location Source', 'Magnitude Source', 'Status'
    ]
    df_load = df.drop(drop_cols, axis=1)
    df_load = df_load.rename(columns={
        "Magnitude Type": "Magnitude_Type",
    })
    print(df_load.head())

    # Insert records into the Quake model/table
    print("Inserting records into PostGreSQL")
    for index, row in df_load.iterrows():
        Date = row['Date']
        Latitude = row['Latitude']
        Longitude = row['Longitude']
        Type = row['Type']
        Depth = row['Depth']
        Magnitude = row['Magnitude']
        Magnitude_Type = row['Magnitude_Type']
        ID = row['ID']

        Quake(Date=Date, Latitude=Latitude, Longitude=Longitude, Type=Type, Depth=Depth, Magnitude=Magnitude, Magnitude_Type=Magnitude_Type, ID=ID).save()
    print("Finished loading data.")
else:
    print("Table not empty, skipping data load.")
