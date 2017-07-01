#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

# import re

r = requests.get("http://www.imdb.com/chart/top?ref_=nv_mv_250_6")
bs = BeautifulSoup(r.text, "lxml")

# print bs.prettify()

movie_data = []

main_div = bs.body.find(id="main")
chart_top250 = main_div.find(attrs={"data-caller-name": "chart-top250movie"})
list_top250 = chart_top250.find(attrs={"class": "lister-list"})

list_top250_title = list_top250.findAll(attrs={"class": "titleColumn"})
rank = 0;
for titleColumn in list_top250_title:
    rank += 1
    title = titleColumn.a.get_text()
    # print titleColumn.a.get_text()
    yearSpan = titleColumn.find(attrs={"class": "secondaryInfo"})
    yearRaw = yearSpan.get_text()
    year = int(yearRaw[1:5])
    # print year
    
    movie_data.append({
        'Rank': rank,
        'Title': title,
        'Year': year
    })

print movie_data