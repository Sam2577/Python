import requests, openpyxl, sys
from bs4 import BeautifulSoup
from lxml import html

url = 'https://stats.nba.com/player/203999/traditional/'

all_urls = []
        
with requests.session() as s:
    
    res = s.get(url)
    print(res.status_code)
    
    soup = BeautifulSoup(res.content, "html.parser")
    
    elements = soup.findAll(class_=['player-stats__stat-title',
                                          'player-stats__stat-value'])
    
    jokic = soup.select('.player-stats__stat-value')
    jokic_pts = jokic[0].text
    print('jokic\'s pts:', jokic_pts)
        

print("done.")
