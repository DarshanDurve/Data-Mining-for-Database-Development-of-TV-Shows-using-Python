# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:27:33 2019

@author: Shriram
"""


import pandas as pd

#Load the csv file into a data frame
NetflixShows = pd.read_csv('C:\\Users\\shrir\Google Drive (karthikeyan.s@husky.neu.edu)\\INFO_6210\\Assignment_1\\Netflix_Shows.csv', encoding='cp437')

NetflixShows.head()

#Check null values
NetflixShows.isnull().sum()

#Ccheck duplicates
NetflixShows.duplicated()
#Drop duplicates
NetflixShows = NetflixShows.drop_duplicates

#Replace null values in user rating score with mean user rating score
NetflixShows['user rating score'] = NetflixShows['user rating score'].fillna(NetflixShows(['user rating score']).mean())

#rename title to tv_show_names
NetflixShows = NetflixShows.rename(columns={'title': 'tv_show_name'})

NetflixShows.to_csv('TVDB_Netflix_Ratings.csv')

NetflixShows.to_csv('TVDB_Netflix_Ratings.csv', sep='\t')