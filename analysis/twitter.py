
import pandas as pd
import requests
from bs4 import BeautifulSoup

#https://twitter.com/Vontobel/status/1244656148512493570

url = 'http://twitter.com/Quora/status/1244656148512493570'

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
text = soup.find_all(text=True)
pAll = soup.find_all('p')
h2All = soup.find_all('h2')

print('end')






