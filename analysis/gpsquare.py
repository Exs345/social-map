import pandas as pd
from math import radians, cos, sin, asin, sqrt
import csv
import numpy as np

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



daten=pd.read_csv('D:/Programmieren/Zürich2020/locations.csv')
middlepoint=np.zeros((len(daten),3))
daten=daten.to_numpy()
for i,data in enumerate(daten):
       lat1=data[3]
       lon1=data[2]
       lat2=data[5]
       lon2=data[4]
       middlepoint[i, 0] = (lat1 + lat2) / 2
       middlepoint[i, 1] = (lon1 + lon2) / 2
       middlepoint[i, 2] = int(data[1])


twitter=pd.read_csv('D:/Programmieren/Zürich2020/crowdbreaks_tweets_jan_jun_2020_has_place(zurich(25-31.3.2020)).csv')
twitter=twitter.to_numpy()
for j, twt in enumerate(twitter):
       lat3=twt[4]
       lon3=twt[3]
       for i,data in enumerate(daten):
              lat1=data[3]
              lon1=data[2]
              lat2=data[5]
              lon2=data[4]

              if lon1 < lon3<lon2:
                     if lat1 <lat3<lat2:
                            point = middlepoint[i, :]

# was ist in der nähe eines punktes
lat4=point[0]
lon4=point[1]
for i,mid in enumerate(middlepoint):
       dif=haversine(lon4, lat4, mid[1], mid[0])
       if dif<0.15:
              print(mid[2])

print('end')


