import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import pandas as pd
from datetime import date
from datetime import time
import numpy as np
from math import radians, cos, sin, asin, sqrt

def get_tiles_data(munic=261):

    TOKEN_URL = 'https://consent.swisscom.com/o/oauth2/token'

    client_id = 'IIq31EHYARZAqE4ur4ndbRGsVZTKGv5v'
    client_secret = 'WsmE3OAyjOd75d7Y'

    # See https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow.
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    # Fetch an access token.
    oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret)

    # To print token, uncomment the following line
    #print(oauth.access_token)

    # Use the access token to query an endpoint.
    resp = oauth.get(
        'https://api.swisscom.com/layer/heatmaps/demo/grids/municipalities/{0}'.format(munic),
        headers={'scs-version': '2'})
    return(resp)
# Doesn't work for multiple postcodes at ones yet
def create_locations_dataframe(munic=261):
    data = get_tiles_data(munic)
    interm = data.json()['tiles']
   # print(len(interm))
   # output=np.zeros((len(interm),5))
    output = pd.DataFrame()
    output['titleId'] = [sub['tileId'] for sub in interm]
    output['ll_x'] = [sub['ll']['x'] for sub in interm]
    output['ll_y'] = [sub['ll']['y'] for sub in interm]
    output['ur_x'] = [sub['ur']['x'] for sub in interm]
    output['ur_y'] = [sub['ur']['y'] for sub in interm]
    #output.to_csv("locations.csv", sep=",", header=True)
    return output




def haversine(lon1, lat1, lon2, lat2):
       """
       Calculate the great circle distance between two points
       on the earth (specified in decimal degrees)
       """
       # convert decimal degrees to radians
       lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
       # haversine formula
       dlon = lon2 - lon1
       dlat = lat2 - lat1
       a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
       c = 2 * asin(sqrt(a))
       # Radius of earth in kilometers is 6371
       km = 6371* c
       return km

#daten=pd.read_csv('C:/Users/Jann/Downloads/locations.csv')
daten= create_locations_dataframe()
middlepoint=np.zeros((len(daten),3))
daten=daten.to_numpy()
for i,data in enumerate(daten):
       lat1=data[2]
       lon1=data[1]
       lat2=data[4]
       lon2=data[3]
       middlepoint[i, 0] = (lat1 + lat2) / 2
       middlepoint[i, 1] = (lon1 + lon2) / 2
       middlepoint[i, 2] = int(data[0]) #id

#not needed.
lat3= 47.38625170  #gps lat
lon3= 8.52872890
for i,data in enumerate(daten):
              lat1=data[2]
              lon1=data[1]
              lat2=data[4]
              lon2=data[3]

              if lon1 < lon3<lon2:
                     if lat1 <lat3<lat2:
                            point = middlepoint[i, :]

# was ist in der nähe eines punktes
lat4=point[0]
lon4=point[1]
ids_New= []
ids_New.append(int(point[2]))

#for i,mid in enumerate(middlepoint):
#       dif=haversine(lon4, lat4, mid[1], mid[0])
#       if dif<0.15:
#              ids_New.append(int(mid[2]))


#create_locations_dataframe(munic=261)
#print(get_tiles_data().json())

def get_tiles_ids(munic=261):
    data = get_tiles_data(munic)
    interm = data.json()['tiles']
    ids = [sub['tileId'] for sub in interm]
    return(ids)

#res = get_tiles_ids(261)
res = ids_New
def format_ids(ids):
    # ids: list of integers
    # Returns: list
    output ='?'
    count = 0
    outputs = []
    for i in ids:
        output = output + 'tiles=' + str(i) + "&"
        count += 1
        if count >= 99:
            outputs.append(output[:(len(output)-1)])
            output = '?'
            count = 0

    if len(ids) >= 100:
        return outputs
    else:
        return [output[:(len(output)-1)]]

print(len(format_ids(res))) # We need to process 8 batches

print(format_ids(res)) # Output for list


#--------------------------------------------------------

def get_time_frame():
    days1 = 25
    days2 = 31
    years1 = 2019
    years2 = 2021
    hours1 = 0
    hours2 = 23
    res = []
    for i in range(years1, years2):
        if i==2020:
            days1=23
            days2 = 30
        for k in range(days1, days2):
            for l in range(hours1, hours2):
               t = str(time(l, 0, 0))
               x = date(i, 3, k)
               res.append(str(x) + 'T' + str(t[:5]))
    return(res)

# Only extract from 6 to 23
time_frame = get_time_frame()
print(time_frame)

def get_density_data(date, formatted_ids):

    # formatted_ids needs to be a list (output of format_ids)
    data = []
    for i in range(len(formatted_ids)):
        TOKEN_URL = 'https://consent.swisscom.com/o/oauth2/token'

        client_id = 'uFdtRJaDao6ATC2kW4WPLCkm2Ywb3Cjg'
        client_secret = '98wsTlX4ou7n1CrD'

        # See https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow.
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)

        # Fetch an access token.
        oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret)

        # To print token, uncomment the following line
        #print(oauth.access_token)

        # Use the access token to query an endpoint.
        resp = oauth.get(
            'https://api.swisscom.com/layer/heatmaps/demo/heatmaps/dwell-density/hourly/{0}{1}'.format(date, formatted_ids[i]),
            headers={'scs-version': '2'})

        output = resp.json()['tiles']
        for key_val in output:
            key_val['time'] = date
        data.append(output)

    print(i)
    return(data)


df = []
for i in range(len(time_frame)):
    df.extend(get_density_data(time_frame[i], format_ids(res)))
#print(len(df))
dt=np.zeros((len(df),3))
outPut=[]
#Head
line= "tileId,score,time"
outPut.append(line)
for i,d in enumerate(df):
    print(d)
    d=d[0]
    temp = str(d['tileId'])+","
    temp += str(d['score'])+","
    temp += str(d["time"])

    outPut.append(temp)

#Export to txt File
MyFile=open('target.txt','w')
for element in outPut:
     MyFile.write(element)
     MyFile.write('\n')
MyFile.close()





