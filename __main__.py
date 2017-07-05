#!/usr/bin/env python
#encoding: utf-8

import requests
from bs4 import BeautifulSoup

import re

def get_link_from_douban(movie_title):
    prefix = 'https://www.douban.com/search?source=suggest&q='
    
    # replace the 'blank' in title to '+'
    # 'The Shawshank Redemption' change to 'The+Shawshank+Redemption'
    douban_query_link = prefix + movie_title
    douban_query_link = re.sub(r' ', '+', douban_query_link)
    # print query_title

    r = requests.get(douban_query_link)
    bs = BeautifulSoup(r.text, "lxml")
    
    query_result_content_div = bs.body.find(id='content')
    result_list_div = query_result_content_div.findAll(attrs={"class": "title"})

    movie_link = ''
    
    for title_div in result_list_div:
        movie_page_prefix = 'https://movie.douban.com/subject/'
        movie_link = ''
        need_type = '电影'
        print need_type.decode('utf8')
        
        type_in_Chinese = title_div.h3.span.get_text()
        print type_in_Chinese
        # print title_div.h3.span.find_next_siblings("span")
        
        if re.search(need_type.decode('utf8'), unicode(type_in_Chinese, 'utf8')):
            
            # if the type is movie
            href_tag = title_div.a
            # query_title = href_tag.get('href', None)
            
            click_args = href_tag.get('onclick', None)
    
            movie_sid = re.search(r'sid: \d*', click_args)
            
            if movie_sid is None:
                print 'Cannot find sid in ' + click_args
            else:
                movie_sid = re.sub(r'\D', '', movie_sid.group())
                # print movie_sid
                movie_link = movie_page_prefix + movie_sid + '/'
            
        break
    
    print movie_link
    
    return movie_link

r = requests.get("http://www.imdb.com/chart/top?ref_=nv_mv_250_6")
bs = BeautifulSoup(r.text, "lxml")

# print bs.prettify()

movie_data = []

main_div = bs.body.find(id="main")
chart_top250 = main_div.find(attrs={"data-caller-name": "chart-top250movie"})
list_top250 = chart_top250.find(attrs={"class": "lister-list"})

list_top250_title = list_top250.findAll(attrs={"class": "titleColumn"})
rank = 0
for titleColumn in list_top250_title:
    rank += 1
    title = titleColumn.a.get_text().encode('utf-8')
    # print titleColumn.a.get_text()
    yearSpan = titleColumn.find(attrs={"class": "secondaryInfo"})
    yearRaw = yearSpan.get_text()
    year = int(yearRaw[1:5])
    # print year
    
    link = get_link_from_douban(title)
    
    movie_data.append({
        'Rank': rank,
        'Year': year,
        'Title': title,
        'Link': link
    })
    break

# print movie_data

movie_file = open('IMDB_top_250.txt', 'w+')

movie_file.write('Rank\tYear\tTitle\tLink\n')

for movie in movie_data:
    # print movie
    movie_info = str(movie['Rank']) + "\t" + str(movie['Year']) + '\t' + movie['Title'] + '\t' + movie['Link'] + '\n'
    movie_file.write(movie_info)

movie_file.close()
