import csv
import json
from re import A, I
from tkinter import Y
from turtle import shape
import pandas as pd
import requests
import folium
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go # for data visualization
import plotly.express as px # for data visualization
import folium.plugins
import branca
import branca.colormap as cm
np.set_printoptions(precision=6, suppress=True)

print('start')

fname = 'colorbartest1211.html'

# 출발과 도착 경로 삭제 => 셔틀차량이 반복적으로 움직이는 경로에 타겟
colorbar_data_set = pd.read_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/colorbar.csv')
print(colorbar_data_set)
f_map = folium.Map(location=[37.410948,127.099298],tiles="OpenStreetMap",zoom_start=14)

latitude = colorbar_data_set["latitude"].tolist()
longitude = colorbar_data_set["longitude"].tolist()
Risk_predict = colorbar_data_set["Risk_Score_pre"].tolist()
Risk_actual = colorbar_data_set["Risk_Score_act"].tolist()
print
colormap = cm.LinearColormap(colors=['blue', 'cyan', 'yellow', 'red'],
                             index=[7,9,11,13], vmin=7, vmax=13,
                             caption='Risk score')

fg = folium.FeatureGroup(name=fname.split('.')[0])  

for index in range(1310):
    color = colormap(Risk_actual[index])
    fg.add_child(folium.CircleMarker(location=[latitude[index],longitude[index]],
                                     radius=3,
                                     fill=True,
                                     color=color,
                                     fill_color=color))



                                     

f_map.add_child(fg)
f_map.add_child(colormap)                                     
f_map.save(fname)
