import csv
import json
from re import A, I
import pandas as pd
import requests
import folium
import numpy as np
import math

print('start')
path = pd.read_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/totaldataset3.csv')

m = folium.Map(location=[37.410948,127.099298],zoom_start=14)

for i in range(0,487):
    i1 = i*10
    folium.Marker(location=[path['latitude'][i1],path['longitude'][i1]],popup='37.410948,127.099298',icon=folium.Icon(color='red',icon='star')).add_to(m)

m.save('shuttle_path.html')


print('end')