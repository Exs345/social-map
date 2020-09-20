import sys
import os
import numpy as np
import pandas as pd
import datetime
from xgboost.sklearn import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')



y = pd.read_csv("target.txt")
y = y.sort_values(by="time", ascending=True).iloc[144:,1].reset_index(drop=True)


#--------------------------------------------------------------------------------
# Weather
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Data/weather/wetter_2020_ZH.txt"
abs_file_path = os.path.join(script_dir, rel_path)
weather_2020 = pd.read_csv(abs_file_path)
rel_path = "Data/weather/wetter_2019_ZH.txt"
abs_file_path = os.path.join(script_dir, rel_path)
weather_2019 = pd.read_csv(abs_file_path)



#print(weather_2020)

def retrieve_date(date):
    # date: str in format year-month-day
    date_list = date.split(sep="-")
    return(datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])))

def find_weather_features(date):
    # date: needs to be a date object

    base = retrieve_date("2020-03-23")
    mult = (retrieve_date(date)-base).days + 1

    if base == date:
        w_3 = weather_2020.iloc[24:48, 1:3].rename(
            columns={"Temp": "temp_3", "precip": "prec_3"}).reset_index(drop=True) # , "Description": "class_3"
        w_2 = weather_2020.iloc[48:72, 1:3].rename(
            columns={"Temp": "temp_2", "precip": "prec_2"}).reset_index(drop=True) # , "Description": "class_2"
        w_1 = weather_2020.iloc[72:96, 1:3].rename(
            columns={"Temp": "temp_1", "precip": "prec_1"}).reset_index(drop=True) # , "Description": "class_1"
    else:
        start = mult * 24

        w_3 = weather_2020.iloc[start:(start+24), 1:3].rename(
            columns={"Temp": "temp_3", "precip": "prec_3"}).reset_index(drop=True) # , "Description": "class_3"
        w_2 = weather_2020.iloc[(start+24):(start+24*2), 1:3].rename(
            columns={"Temp": "temp_2", "precip": "prec_2"}).reset_index(drop=True) # , "Description": "class_2"
        w_1 = weather_2020.iloc[(start+24*2):(start+24*3), 1:3].rename(
            columns={"Temp": "temp_1", "precip": "prec_1"}).reset_index(drop=True) # , "Description": "class_1"

    return (pd.concat([w_3, w_2, w_1], axis=1))

#print(find_weather_features("2020-03-23"))

dates = ["2020-03-2{0}".format(i) for i in range(3, 10)]
feature_matrices = [find_weather_features(date) for date in dates]

weather_features_final = pd.concat(feature_matrices, axis=0).reset_index(drop=True)

#--------------------------------------------------------------------------------
# Covid Cases
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Data/covid_19_data_switzerland_filtered.csv"
abs_file_path = os.path.join(script_dir, rel_path)
cases = pd.read_csv(abs_file_path, sep=";")

# Only get Zurich data in relevant data range
start = list(cases["Date"]).index("2020-03-20")
end = list(cases["Date"]).index("2020-03-26")

cases = cases.iloc[start:(end+1),:]
cases_adj = cases.loc[:,"ZH"]

# Replicate data to be available hourly
cases_final = np.repeat(cases_adj, 24).reset_index(drop=True)

#--------------------------------------------------------------------------------
# Covid Deaths
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Data/covid_19_data_switzerland_filtered_dead.csv"
abs_file_path = os.path.join(script_dir, rel_path)

deaths = pd.read_csv(abs_file_path, sep=";")

# Only get Zurich data in relevant data range
start = list(deaths["Date"]).index("2020-03-20")
end = list(deaths["Date"]).index("2020-03-26")

deaths = deaths.iloc[start:(end+1),:]
deaths_adj = deaths.loc[:,"ZH"]

# Replicate data to be available hourly
deaths_final = np.repeat(deaths_adj, 24).reset_index(drop=True)

#--------------------------------------------------------------------------------
# Newspaper Titles (3 days before)
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Data/NewsSRF/outputData_2.csv"
abs_file_path = os.path.join(script_dir, rel_path)

newspaper = pd.read_csv(abs_file_path, index_col=False)
newspaper_sorted = newspaper.sort_values(by=['Day'], ascending=True).reset_index(drop=True).iloc[4:11,1:4]
all = np.repeat(newspaper_sorted["All"] , 24)
perc_rel = np.repeat(newspaper_sorted["AllRelevant"]/newspaper_sorted["All"] , 24)
perc_zur = np.repeat(newspaper_sorted["AllZurich"]/newspaper_sorted["All"] , 24)

newspaper_final = pd.concat([all, perc_rel, perc_zur], axis=1).rename(columns={"All": "articl", 0:"perc_rel", 1:"perc_zur"}).reset_index(drop=True)
#print(newspaper_final)

#--------------------------------------------------------------------------------
# Mobility
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "Data/mobility_ZH_2020.csv"
abs_file_path = os.path.join(script_dir, rel_path)

mobility = pd.read_csv(abs_file_path, sep=";")

mobility.loc[145.5,:] = "2020-03-29T02:00:00", 2897, 554, 982
mobility_final = mobility.sort_index().reset_index(drop=True).iloc[:,1:4].rename(columns={"Total": "trips", "Incoming": "incoming", "Innside": "inside"})
#print_full(mobility_final)

#---------------------------------------------------------------------------------
# Final feature matrix

X = pd.concat([weather_features_final, newspaper_final, mobility_final], axis=1).dropna()

#---------------------------------------------------------------------------------
# Regression

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
model = XGBRegressor(objective="reg:squarederror")
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(y_pred)
print(y_test)




print(cross_val_score(model, X, y, cv=5))
#
# model.fit(X, y)
#
# # Supply values here
# X_test =
# y_test = model.predict(X_test)
