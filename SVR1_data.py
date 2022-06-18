import csv
import json
from re import A, I
import pandas as pd
import requests
import folium
import numpy as np
import math
import matplotlib.pyplot as plt


print('start')

df_gps_list = []
df_obs_list = []


# data save for gps
for pagenumber_str in range(1, 10):
    url = 'http://apis.data.go.kr/C100006/zerocity/getGpsInsList'
    params ={'serviceKey' : '3kpELyLZTv9YXuOkoCFeHxl82DIu4FUxmsdBWPjPx1AsgGm8PBj+iUGerHsfvtbNlYNNRy8djNsXAKzcHcj53A==', 'type' : '', 'numOfRows' : '1000', 'pageNo' : pagenumber_str , 'startDt' : '2021-11-11', 'endDt' : '2021-11-12' }
    response = requests.get(url, params=params)
    # print(response.content)
    pagedata = response.json()
    df_gps = pd.DataFrame(data=response.json()[0]['gpsInsFileList'])
    df_gps_data = df_gps[['ss_num','nano_ss_num','latitude', 'longitude', 'altitude']]
    df_gps_data.to_json('getGpsInsList_{}.json'.format(pagenumber_str))
   
# data read for gps 
for pagenumber_str in range(1, 489):
    df_gps_data = pd.read_json('getGpsInsList_{}.json'.format(pagenumber_str))
    df_gps_list.append(df_gps_data)


df_gps = pd.concat(df_gps_list)
df_gps.reset_index(inplace=True)
df_gps1 = df_gps.drop(columns = ['index'],axis=1)

df_gps1 = df_gps.drop_duplicates(['ss_num'])
df_gps1.reset_index(inplace=True)
df_gps2 = df_gps1.drop(columns = ['index'],axis=1)
print(df_gps2)
print(df_gps2.shape)
print(type(df_gps2))
#data save for obstacle
for pagenumber_str in range(1, 217):
    url = 'http://apis.data.go.kr/C100006/zerocity/getObstacleList'
    params ={'serviceKey' : '3kpELyLZTv9YXuOkoCFeHxl82DIu4FUxmsdBWPjPx1AsgGm8PBj+iUGerHsfvtbNlYNNRy8djNsXAKzcHcj53A==', 'type' : '', 'numOfRows' : '1000', 'pageNo' : pagenumber_str, 'startDt' : '2021-11-11', 'endDt' : '2021-11-30' }
    response = requests.get(url, params=params)
    # print(response.content)
    pagedata = response.json()
    df_obs = pd.DataFrame(data=response.json()[0]['obstacleFileList'])
    df_obs_data = df_obs[['ss_num','nano_ss_num','drv_stts_cd','obcl_type_cd','obcl_stts_cd','obcl_size_chng_val','obcl_x_acrat']]
    df_obs_data.to_json('obstacleFileList_{}.json'.format(pagenumber_str))

# data read for obstacle
for pagenumber_str in range(1, 217):
    df_obs_data = pd.read_json('obstacleFileList_{}.json'.format(pagenumber_str))
    df_obs_list.append(df_obs_data)

df_obs = pd.concat(df_obs_list)
df_obs.reset_index(inplace=True)

df_obs1 = df_obs.drop(columns = ['index'],axis=1)
df_obs2 = df_obs1.drop_duplicates(['ss_num'])
df_obs2.reset_index(inplace=True)
df_obs3 = df_obs2.drop(columns = ['index'],axis=1)

df_obs4 = pd.read_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/obstacle_data4874.csv')

Data_tot = pd.concat([df_gps2,df_obs4],axis=1)

time = list(range(4874))
df_time = pd.DataFrame(time,columns=['time(s)'])

Data_tot_time = pd.concat([df_time,Data_tot],axis=1)


Data_tot_time2 = Data_tot_time.drop(columns = ['level_0'],axis=1)
Data_tot_time3 = Data_tot_time2.drop(columns = ['ss_num'],axis=1)
Data_tot_time4 = Data_tot_time3.drop(columns = ['nano_ss_num'],axis=1)
Data_tot_time5 = Data_tot_time4.drop(columns = ['constant'],axis=1)
Data_tot_time6 = Data_tot_time5.drop(columns = ['time'],axis=1)
Data_tot_time7 = Data_tot_time6.drop(columns = ['Unnamed: 0'],axis=1)

#obstacle type 1 : 1-VEHICLE, 2-TRUCK, 3-BIKE, 4-PED, 5-BICYCLE
for i in range(0,4874):
    if Data_tot_time7.loc[i, 'obcl_type_cd'] == 1:
        Data_tot_time7.loc[i, 'Risk Score']= 5
    if Data_tot_time7.loc[i, 'obcl_type_cd'] == 2:
        Data_tot_time7.loc[i, 'Risk Score'] = 5
    if Data_tot_time7.loc[i, 'obcl_type_cd'] == 3:
        Data_tot_time7.loc[i, 'Risk Score'] = 4
    if Data_tot_time7.loc[i, 'obcl_type_cd']== 4:
        Data_tot_time7.loc[i, 'Risk Score']= 2
    if Data_tot_time7.loc[i, 'obcl_type_cd']== 5:
        Data_tot_time7.loc[i, 'Risk Score'] = 2


#obstacle status type 1-UNDEFINED, 2-STANDING, 3-STOPPED, 4-MOVING, 5-ONCOMING, 6-PARKED
for i in range(0,4874):
    if Data_tot_time7.loc[i, 'obcl_stts_cd'] == 1:
        Data_tot_time7.loc[i, 'Risk Score1']= 1
    if Data_tot_time7.loc[i, 'obcl_stts_cd'] == 2:
        Data_tot_time7.loc[i, 'Risk Score1'] = 1
    if Data_tot_time7.loc[i, 'obcl_stts_cd'] == 3:
        Data_tot_time7.loc[i, 'Risk Score1'] = 1
    if Data_tot_time7.loc[i, 'obcl_stts_cd']== 4:
        Data_tot_time7.loc[i, 'Risk Score1']= 4
    if Data_tot_time7.loc[i, 'obcl_stts_cd']== 5:
        Data_tot_time7.loc[i, 'Risk Score1'] = 5
    if Data_tot_time7.loc[i, 'obcl_stts_cd']== 6:
        Data_tot_time7.loc[i, 'Risk Score1'] = 1   


#Driving status 01-STOP, 02-GO, 03-UNDECIDED, 04-DRIVER_DECISION_REQUIRED, 05-NOT_CALCULATED
for i in range(0,4874):
    if Data_tot_time7.loc[i, 'drv_stts_cd'] == 1:
        Data_tot_time7.loc[i, 'Risk Score2']= 1
    if Data_tot_time7.loc[i, 'drv_stts_cd'] == 2:
        Data_tot_time7.loc[i, 'Risk Score2'] = 4
    if Data_tot_time7.loc[i, 'drv_stts_cd'] == 3:
        Data_tot_time7.loc[i, 'Risk Score2'] = 2
    if Data_tot_time7.loc[i, 'drv_stts_cd']== 4:
        Data_tot_time7.loc[i, 'Risk Score2']= 5
    if Data_tot_time7.loc[i, 'drv_stts_cd']== 5:
        Data_tot_time7.loc[i, 'Risk Score2'] = 0

#obstacle acceleration 
#Forward direction moving obstacle
for i in range(0,4874):
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] > 0 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 0.5 : 
        Data_tot_time7.loc[i, 'Risk Score3']= 1
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 0.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 1 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 1
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 1 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 1.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 2
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 1.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 2 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 2
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 2 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 2.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 3        
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 2.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 3 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 3 
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 3 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 3.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 4        
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 3.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < 4 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 4        
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= 4 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 5
#opposite direction moving obstacle
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] > -0.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] <= 0 : 
        Data_tot_time7.loc[i, 'Risk Score3']= 1
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -1 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -0.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 1
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -1.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -1 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 2
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -2 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -1.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 2
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -2.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -2 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 3        
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -3 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -2.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 3 
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -3.5 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -3 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 4        
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] >= -4 and Data_tot_time7.loc[i, 'obcl_x_acrat'] < -3.5 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 4        
    if Data_tot_time7.loc[i, 'obcl_x_acrat'] <= -4 : 
        Data_tot_time7.loc[i, 'Risk Score3'] = 5




Data_tot_time7['Risk_Score_Tot'] = Data_tot_time7['Risk Score'] + Data_tot_time7['Risk Score1'] + Data_tot_time7['Risk Score3']
Data_tot_time7['Risk_Score_Mul'] = Data_tot_time7['Risk Score'] * Data_tot_time7['Risk Score1']* Data_tot_time7['Risk Score3']
for i in range(0,4874):
    Data_tot_time7.loc[i, 'Risk_Score_exp'] = math.exp(Data_tot_time7.loc[i, 'Risk_Score_Tot']) 

for i in range(0,4874):
    Data_tot_time7.loc[i, 'Risk_Score_exp_div'] = (Data_tot_time7.loc[i, 'Risk_Score_exp'])/100 

for i in range(0,4874):
    if Data_tot_time7.loc[i, 'Risk_Score_exp_div'] > 10000 : 
        Data_tot_time7.loc[i, 'High_Risk']= Data_tot_time7.loc[i, 'Risk_Score_exp_div']
    if Data_tot_time7.loc[i, 'Risk_Score_exp_div'] <= 10000 : 
        Data_tot_time7.loc[i, 'High_Risk']= 0        

print(Data_tot_time7)
print(Data_tot_time7.shape)
print(type(Data_tot_time7))
Data_tot_time7.to_csv('C:/Users/bhj/Desktop/Hyznbyn/2022_1/ML/totaldataset3.csv')

