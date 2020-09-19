import requests
import csv
import pandas
#API DATA
cAdress= "https://api.weatherbit.io/v2.0/history/hourly?lat={}&lon={}&start_date={}&end_date={}&key={}"
cLat="46.204391"
cLong=" 6.143158"
cAppid="26cc1600ca1a4b20a18f6075847f2137"
cDat="2019-03-"
cDat2="2019-03-"

# String List
outPut=[]
#Head
line= "Date,Temp,precip,Description"
outPut.append(line)
for i in range(24,31):
    test = cAdress.format (cLat, cLong,cDat,cDat2,cAppid)
    #Data hourly for 1 day, free subscription limitation
    city_weather = requests.get(cAdress.format (cLat, cLong,cDat+str(i),cDat2+str(i+1),cAppid)).json()
    day= city_weather['data']
    for hour in day:
        temp = str(hour['timestamp_utc'])+","
        temp += str(hour['temp'])+","
        temp += str(hour["precip"])+","
        temp +=str(hour['weather']["description"])
        outPut.append(temp)
#Export to txt File
MyFile=open('output.txt','w')
for element in outPut:
     MyFile.write(element)
     MyFile.write('\n')
MyFile.close()


