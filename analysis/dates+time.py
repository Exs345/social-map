
import arrow
import numpy as np
import pandas as pd
from datetime import date
from datetime import time


#2020-03-26T09:00
days1=23
days2=31
months1=3
months2=4
years1=2020
years2=2021
hours1=0
hours2=24
for i in range(years1,years2):
       for j in range(months1,months2):
              for k in range(days1,days2):
                     for l in range(hours1,hours2):
                            t = str(time(l, 0, 0))
                            x = date(i, j, k)
                            print(str(x)+'T'+str(t[:5]))
print('Ende')







