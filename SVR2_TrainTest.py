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

print('start')

# 출발과 도착 경로 삭제 => 셔틀차량이 반복적으로 움직이는 경로에 타겟
data_set = pd.read_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/6part.csv')

for i in range(0,4220):
        data_set.loc[i, 'latitude_norm']= data_set.loc[i, 'latitude']-data_set['latitude'].mean()
        data_set.loc[i, 'longitude_norm']= data_set.loc[i, 'longitude']-data_set['longitude'].mean()

# data_set.to_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/6part00.csv')

Train_data_set = data_set.loc[ :2909, : ]
Train_latitude_norm = Train_data_set['latitude_norm']
Train_longitude_norm = Train_data_set['longitude_norm']
Train_Risk_Score_expdiv = Train_data_set['Risk_Score_Tot']

Test_data_set = data_set.loc[ 2910: , : ]
Test_latitude_norm = Test_data_set['latitude_norm']
Test_longitude_norm = Test_data_set['longitude_norm']
Test_Risk_Score_expdiv = Test_data_set['Risk_Score_Tot']

print(Test_data_set)
stdscaler = StandardScaler()
#Training data
X1 = stdscaler.fit(Train_latitude_norm.values.reshape(-1,1)).transform(Train_latitude_norm.values.reshape(-1,1))
X2 = stdscaler.fit(Train_longitude_norm.values.reshape(-1,1)).transform(Train_longitude_norm.values.reshape(-1,1))
Y = stdscaler.fit(Train_Risk_Score_expdiv.values.reshape(-1,1)).transform(Train_Risk_Score_expdiv.values.reshape(-1,1))
#Test data
XX1 = stdscaler.fit(Test_latitude_norm.values.reshape(-1,1)).transform(Test_latitude_norm.values.reshape(-1,1))
XX2 = stdscaler.fit(Test_longitude_norm.values.reshape(-1,1)).transform(Test_longitude_norm.values.reshape(-1,1))
YY = stdscaler.fit(Test_Risk_Score_expdiv.values.reshape(-1,1)).transform(Test_Risk_Score_expdiv.values.reshape(-1,1))

Scaled_x1x2 = np.concatenate([X1,X2],axis=1)
Scaled_xx1xx2 = np.concatenate([XX1,XX2],axis=1)
print(Scaled_xx1xx2)
train_data_set_scaled = pd.DataFrame(Scaled_x1x2, columns = ['latitude(scaled)','longitude(scaled)'])
train_totaldata = pd.concat([Train_data_set,train_data_set_scaled],axis=1)

test_data_set_scaled = pd.DataFrame(Scaled_xx1xx2, columns = ['latitude(scaled)','longitude(scaled)'])
Test_data_set.reset_index(inplace=True)
test_data_set_scaled.reset_index(inplace=True)
test_totaldata = pd.concat([Test_data_set,test_data_set_scaled],axis=1)

test_totaldata.to_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/Test_data_set11.csv')

train_totaldata.to_numpy()
test_totaldata.to_numpy()

X_train=train_totaldata[['latitude(scaled)','longitude(scaled)']]
y_train=train_totaldata['Risk_Score_Tot'].values

X_test=test_totaldata[['latitude(scaled)','longitude(scaled)']]
y_test=test_totaldata['Risk_Score_Tot'].values

Model2 = SVR(kernel='rbf', C=100, epsilon=1)

svr = Model2.fit(X_train, y_train)
#-----------------훈련끝-----------------#

x_data = test_totaldata[['latitude(scaled)']].to_numpy()
y_data = test_totaldata[['longitude(scaled)']].to_numpy()
pred_svr = svr.predict(np.c_[x_data.ravel(), y_data.ravel()])

print(x_data)
print(x_data.shape)
print(type(x_data))
print(y_data)
print(y_data.shape)
print(type(y_data))

pred_svr = svr.predict(np.c_[x_data.ravel(), y_data.ravel()])
print(x_data.ravel())
print(x_data.ravel().shape)
print(type(x_data.ravel()))

print(y_data.ravel())
print(y_data.ravel().shape)
print(type(y_data.ravel()))

print(pred_svr)
print(pred_svr.shape)
print(type(pred_svr))
print(pred_svr)
print(pred_svr.shape)
print(type(pred_svr))
df_pred_svr=pd.DataFrame(pred_svr)

DF = pd.DataFrame(pred_svr)
DF.to_csv("predict_Y3.csv")

print('end')