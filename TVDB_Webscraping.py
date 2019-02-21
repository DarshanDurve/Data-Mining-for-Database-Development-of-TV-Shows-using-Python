# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:54:01 2019

@author: Darshan Durve
"""

from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd

# Getting the html response from the 50 popular TV shows IMDB webpage:

url = "https://www.imdb.com/search/title?title_type=tv_series"
response = get(url)
html_soup = bs(response.text ,'html.parser')
id_check = html_soup.find(id ="main")
tv_show_container = id_check.find_all(class_ ="lister-item mode-advanced")
container = tv_show_container[0]

# list to store scraped value data in:

tv_show_names = []
year_release = []
imdb_ratings = []
votes = []
tv_show_description = []
runtime = []
genre = []
star_cast = []
title_Id = []

# Scraping the data by looping through the webpage:

for container in tv_show_container:

    if container.find("div", class_ = "ratings-bar") is not None:

        name = container.h3.a.text
        tv_show_names.append(name)

        Id = container.img['data-tconst']
        title_Id.append(Id)

        release = container.find("span", class_ = "lister-item-year text-muted unbold").text
        year_release.append(release)

        ratings = float(container.strong.text)
        imdb_ratings.append(ratings)

        vote = container.find("span", attrs = {"name" :"nv"})['data-value']
        votes.append(int(vote))

        run = container.find("span", class_ ="runtime").text
        runtime.append(run)

        gen = container.find("span", class_ ="genre").text.strip()
        genre.append(gen)

        content = container.find_all("p")

        desc = content[1].text.strip()
        tv_show_description.append(desc)

        content_2 = content[2].find_all("a")

        temp = []
        for i in range(len(content_2)):
            temp.append(content_2[i].text)
        star_cast.append(temp)


# Putting the TV show information into a Pandas DataFrame:

tv_show_df = pd.DataFrame({"tv_show_name" :tv_show_names,
                        "tv_show_id" :title_Id,
                        "start_and_end_year" :year_release,
                        "imdb_rating" :imdb_ratings,
                        "votes" :votes,
                        "tv_show_description" :tv_show_description,
                        "runtime" :runtime,
                        "genre" :genre,
                        "star_cast": star_cast,
                        })

# Getting the season information of the TV shows:
# list to store scraped value data in & variable assignments:

title_Id = []
epi_name = []
c1 = []
b = []
n = []
m = []
x= []
u = []
y = 1

# Scraping the season data by looping through the webpage:
# Generating the URL for the maximum number of seasons to scrape the data from:

for index, row in tv_show_df.iterrows():
    x = str(row['tv_show_id'])
    url_season = 'https://www.imdb.com/title/' + x + '/?ref_=adv_li_tt'

    response = get(url_season)
    html_soup = bs(response.text, 'html.parser')

    id_check = html_soup.find(id="main_bottom")
    episode_container = id_check.find(class_="seasons-and-year-nav")

    total_seasons = episode_container.a.text
    total_seasons = int(total_seasons)

    while y <= total_seasons:
        
        url = 'https://www.imdb.com/title/' + x + '/episodes?season=' + str(y)
        response = get(url)
        html_soup = bs(response.text, 'html.parser')
        id_check = html_soup.find(id="main")
        episode_container = id_check.find_all(class_="list_item")
        len(episode_container)
        epi_container = episode_container[0]
        c = 0
        
        for epi_container in episode_container:

            if epi_container.find("div", class_="ipl-rating-widget") is not None:
                
                id_1 = epi_container.div.a.find('div', class_="hover-over-image")['data-const']
                title_Id.append(id_1)

                name = epi_container.a['title']
                epi_name.append(name)

                c += 1
                c1.append(c)

        b.extend(title_Id)
        n.extend(epi_name)
        m.extend(c1)
        
        title_Id.clear()
        epi_name.clear()
        c1.clear()
        
        y += 1
        
    y = 1


# Putting the season wise information into a Pandas DataFrame:
    
season_df = pd.DataFrame({"title_id": b,
                   'episode_name': n,
                   'episode_number': m})


# Getting the episode details of individual TV shows information:
# list to store scraped value data in & variable assignments:

episode_name = []
duration = []
epi_ratings = []
votes = []
tv_show_name = []
director = []
season_name = []
x = []
g = []
h = []
j = []
k = []
l = []
f = []
y = 1

# Scraping the episode data by looping through the webpage:
# Generating the URL to scrape the data:

for index, row in season_df.iterrows():
    x = str(row['title_id'])
    y = str(row['episode_number'])
    url_1 = 'https://www.imdb.com/title/' + x + '/?ref_=ttep_ep' + y
    response = get(url_1)
    html_soup = bs(response.text, 'html.parser')
    id_check = html_soup.find(id="main_top")
    episode_container = id_check.find_all(class_="heroic-overview")
    epi_container = episode_container[0]

    for epi_container in episode_container:

        if epi_container.find("div", class_="title_block") is not None:

            name = epi_container.find(class_="title_wrapper").h1.text.strip()
            episode_name.append(name)

            time = epi_container.find(class_="subtext").time.text.strip()
            duration.append(time)

            try:
                rat = epi_container.find(class_="ratingValue").strong.span.text
                epi_ratings.append(rat)
            except:
                epi_ratings.append('NA')

            title = epi_container.find(class_="titleParent").a.text
            tv_show_name.append(title)

            try:
                dir = epi_container.find(class_="credit_summary_item").a.text
                director.append(dir)
            except:
                director.append('NA')

            s_name = epi_container.find(class_="bp_heading").text
            season_name.append(s_name)

    g.extend(episode_name)
    h.extend(duration)
    f.extend(epi_ratings)
    j.extend(tv_show_name)
    k.extend(director)
    l.extend(season_name)
    
    episode_name.clear()
    duration.clear()
    tv_show_name.clear()
    director.clear()
    season_name.clear()

# Putting the episode wise information into a Pandas DataFrame:

a = {"episode_name": g,
     "tv_show_name": j,
     "imdb_ratings": epi_ratings,
     "runtime_in_mins": h,
     "director": k,
     "season": l}

episode_df = pd.DataFrame.from_dict(a, orient='index')
episode_df = episode_df.transpose()


##Data Cleaning:

episode_df['runtime_in_mins'] = episode_df.runtime_in_mins.str.replace('[^0-9]', '')
episode_df['runtime_in_mins'].astype('int64')

tv_show_df['runtime'] = tv_show_df.runtime.str.replace('[^0-9]', '')
tv_show_df['runtime'].astype('int64')

tv_show_df['start_and_end_year'] = tv_show_df.start_and_end_year.str.replace('[^0-9]', ' ')
tv_show_df['start_and_end_year'] = tv_show_df.start_and_end_year.str.replace(' ','')

tv_show_df['start_year'] = tv_show_df.start_and_end_year.str.slice(0, 4)
tv_show_df['end_year'] = tv_show_df.start_and_end_year.str.slice(4, 8)
tv_show_df['start_year'].astype('int64')

tv_show_df = tv_show_df.drop(columns=['start_and_end_year'])

##Converting to csv

tv_show_df.to_csv('TV_Show_Entity.csv')
episode_df.to_csv('Episode_Entity.csv')












