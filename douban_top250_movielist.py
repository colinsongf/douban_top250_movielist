import requests
from bs4 import BeautifulSoup
import csv

init_url='http://movie.douban.com/top250'

def get_html(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    html=requests.get(url,headers=headers)
    return html.content

def parse_html(html):
    soup=BeautifulSoup(html,'lxml')
    movie_list_soup = soup.find('ol', {'class': 'grid_view'})
    movie_name_list=[]
    for movie_li in movie_list_soup.find_all('li'):
        movie_name = movie_li.find('span', {'class': 'title'}).get_text()
        movie_name_list.append(movie_name)
    next_page=soup.find('span',{'class':'next'}).find('a')
    if next_page:
        return movie_name_list,init_url+next_page['href']
    return movie_name_list,None

url=init_url
movie_list=[]
csvfile=open('../douban/douban.csv','w+')
try:
    writer=csv.writer(csvfile)
    while url:
        html=get_html(url)
        movies,url=parse_html(html)
        #movie_list.extend(movies)
        writer.writerow(movies)
    #print(movie_list)
finally:
    csvfile.close()