# -*- coding: utf-8 -*-
"""
Market Share Calculator

Author: Federico Scivittaro
Last Updated: 1/25/18

Description
"""

import random
import time
import pandas as pd

from util import open_csv_to_df
from util import save_df_to_csv


def get_season_stats_for_url_list(url_list, func):
    """
    url_list: A list of tea season urls to scrape stats for that team's season
    func: The function to use when scraping
    """
    
    full_pass_dict = {}
    full_rush_rec_dict = {}
    full_defense_dict = {}
    
    i = 1
    
    for url in url_list:

        d1, d2, d3 = func(url)  # Run given function with url as param
    
        full_pass_dict.update(d1)
        full_rush_rec_dict.update(d2)
        full_defense_dict.update(d3)
        
        print(i)
        i += 1
        wait_time = random.randint(15, 60)
        time.sleep(wait_time)
        
    return full_pass_dict, full_rush_rec_dict, full_defense_dict


def calculate_market_shares(df, stat):
    """
    """
    
    team_df = df.groupby(['Team', 'Year'], as_index=True)[stat].agg('sum')
    
    
    def calculate_row_share(row):
        """
        """
        
        team = row['Team']
        year = row['Year']
        
        player_stat = row[stat]
        team_stat = team_df[team][year]
        
        if team_stat == 0:
            share = 0
        else:
            share = round(player_stat / team_stat, 2)
        
        return share
    
    
    new_col = df.apply(lambda row: calculate_row_share(row), axis=1)
    
    return new_col


def append_market_share_data(filename, stats_list):
    """
    """
    
    df = open_csv_to_df(filename, index='PlayerYearID')
    
    for stat in stats_list:
        new_col = stat + ' SHARE'
        df[new_col] = calculate_market_shares(df, stat)
    
    new_filename = filename[:-4] + '_shares.csv'
    
    save_df_to_csv(df, new_filename, col_headers=True, index=True,
               index_label='PlayerYearID', mode='w')
    
    return df