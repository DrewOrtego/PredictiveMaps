from datetime import datetime
import os
import pandas as pd
import numpy as np

from django.contrib import admin
from geoQuakesapp.models import Quake, QuakePredictions
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

admin.site.register(Quake)
admin.site.register(QuakePredictions)

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
    print("Populating Quake table.")
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
    print("Finished loading Quake data.")
else:
    print("Table not empty, skipping data load.")

# Machine learning model data creation
if QuakePredictions.objects.all().count() == 0:
    # Run through the workflow in the jupyter notebook file to populate the table
    earthquakes_csv = r'C:\Users\andr7495\Documents\GitHubDrewOrtego\PredictiveMaps\geoQuakes\static\resources\earthquakeTest.csv'
    database_csv = r'C:\Users\andr7495\Documents\GitHubDrewOrtego\PredictiveMaps\geoQuakes\static\resources\database.csv'

    df_test = pd.read_csv(earthquakes_csv)
    df_train = pd.read_csv(database_csv)

    df_test_load = df_test[['time', 'latitude', 'longitude', 'mag', 'depth']]
    df_train_load = df_train.drop(['Depth Error', 'Time', 'Depth Seismic Stations', 'Magnitude Error', 'Magnitude Seismic Stations', 'Root Mean Square', 'Source', 'Location Source', 'Magnitude Source', 'Status', 'Azimuthal Gap', 'Horizontal Distance', 'Horizontal Error'], axis=1)

    df_test_load = df_test_load.rename(columns={'time': 'Date', 'latitude': 'Latitude', 'longitude': 'Longitude', 'mag': 'Magnitude', 'depth': 'Depth'})
    df_train_load = df_train_load.rename(columns={"Magnitude Type": "Magnitude_Type"})

    # Create training and test dataframes
    df_test_data = df_test_load[['Latitude', 'Longitude', 'Magnitude', 'Depth']]
    df_train_data = df_train_load[['Latitude', 'Longitude', 'Magnitude', 'Depth']]

    # Remove all null values from the datasets
    df_test_data.dropna()
    df_train_data.dropna()

    X_test = df_test_data[['Latitude', 'Longitude']]
    y_test = df_test_data[['Magnitude', 'Depth']]

    X_train = df_train_data[['Latitude', 'Longitude']]
    y_train = df_train_data[['Magnitude', 'Depth']]

    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    # create RFR model, train it
    model_reg = RandomForestRegressor(random_state=50)
    model_reg.fit(X_train, y_train)
    model_reg.predict(X_test)

    parameters = {'n_estimators': [10, 20, 50, 100, 200, 500]}
    grid_obj = GridSearchCV(model_reg, parameters)
    grid_fit = grid_obj.fit(X_train, y_train)
    best_fit = grid_fit.best_estimator_
    results = best_fit.predict(X_test)
    score = best_fit.score(X_test, y_test) * 100
    
    # Use the best fit model to make the prediction on our out-of-sample test data (quakes for 2017)
    final_results = best_fit.predict(X_test)
    final_score = best_fit.score(X_test, y_test) * 100

    lst_magnitudes = []
    lst_depth = []
    for i, r in enumerate(final_results.tolist()):
        lst_magnitudes.append(final_results[i][0])
        lst_depth.append(final_results[i][1])

    df_results = X_test[['Latitude', 'Longitude']]
    df_results['Magnitude'] = lst_magnitudes
    df_results['Depth'] = lst_depth
    df_results['Score'] = final_score

    print("Populating QuakePredictions table.")
    for i, row in df_results.iterrows():
        Latitude = row['Latitude']
        Longitude = row['Longitude']
        Magnitude = row['Magnitude']
        Depth = row['Depth']
        Score = row['Score']

        QuakePredictions(Latitude=Latitude, Longitude=Longitude, Magnitude=Magnitude, Depth=Depth, Score=Score).save()
    print("Finished loading QuakePredictions data.")
else:
    print("Table not empty, skipping data load.")
