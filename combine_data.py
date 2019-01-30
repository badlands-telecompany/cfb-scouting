# -*- coding: utf-8 -*-
"""
Combine Data Scraper

Author: Federico Scivittaro

Date: 12/21/17

Description
"""

from util import get_soup
from util import open_csv_to_df
from util import save_df_to_csv

import pandas as pd
import time
import random
from fake_useragent import UserAgent


def collect_data_by_year(year):
    """
    Scrape combine data for all players for the given year.
    """
    
    # Format page request
    url = 'http://nflcombineresults.com/nflcombinedata_expanded.php'
    headers = {'user-agent': UserAgent().random}
    params = {'year': year}
    
    soup = get_soup(url, headers=headers, params=params)
    
    # Check if the database contains the requested year
    possible_set = set([])
    possible_years = soup.find('select', attrs={'id': 'year'}).find_all('option')
    
    for y in possible_years:
        possible_set.add(y.get_text())
        
    if str(year) not in possible_set:
        return {} # Return empty dict if the year is incompatible
    
    rows = soup.find_all('tr', attrs={'class': 'tablefont'})
    full_dict = {}
    counter = 1

    for row in rows:
        tds = row.find_all('td')
        row_dict = {}
        
        for i, td in enumerate(tds):
            is_hidden = td.find('div', attrs={'style': 'visibility:hidden;'})
            
            # Check if the player has any data for each cell
            if is_hidden:
                text = ''
            else:
                text = td.get_text()
        
            # Add data to a preliminary dict
            row_dict[i] = text
        
        # Assign relevant keys to data
        row_dict['year'] = row_dict.pop(0)
        row_dict['name'] = row_dict.pop(1)
        row_dict['school'] = row_dict.pop(2)
        row_dict['POS'] = row_dict.pop(3)
        row_dict['height'] = row_dict.pop(4)
        row_dict['weight'] = row_dict.pop(5)
        row_dict['handSize'] = row_dict.pop(6)
        row_dict['armLength'] = row_dict.pop(7)
        row_dict['wonderlic'] = row_dict.pop(8)
        row_dict['forty'] = row_dict.pop(9)
        row_dict['bench'] = row_dict.pop(10)
        row_dict['vert'] = row_dict.pop(11)
        row_dict['broad'] = row_dict.pop(12)
        row_dict['shuttle'] = row_dict.pop(13)
        row_dict['3cone'] = row_dict.pop(14)
        row_dict['60shuttle'] = row_dict.pop(15)
        
        # Create unique player code
        name = row_dict['name']
        name_code = name.replace("'", '').replace('.', '').replace(' ', '-').lower()
        key = '{}-{}-{}'.format(name_code, counter, year)
        counter += 1
        
        # Create dict of dicts containing all data
        full_dict[key] = row_dict
    
    return full_dict


def collect_data_for_multiple_years(start_year, end_year, filename):
    """
    Scrape combine data for all players from a range of years.
    """
    
    full_dict = {}
    
    for year in range(start_year, end_year + 1):
        year_dict = collect_data_by_year(year)
        full_dict.update(year_dict) # Create dict of dicts
        
        print(year)
        time.sleep(random.randint(5, 60)) # Sleep to not overwhelm site
        
    # Convert dict of dicts to Pandas df
    df = pd.DataFrame.from_dict(full_dict, orient='index')
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'playerCode'})
    save_df_to_csv(df, filename, col_headers=True, index=True,
                   index_label='idNum', mode='w')
    
    return df


def add_new_data_to_combine_df(year, filename):
    """
    Add newly scraped combine data to alrady-existing csv data file.
    """

    year_dict = collect_data_by_year(year) # Collect new data
    df = open_csv_to_df(filename, index='idNum') # Retrieve other data
    df.set_index('playerCode', inplace=True)
    full_dict = df.to_dict(orient='index')
    full_dict.update(year_dict) # Merge data
    # Create unified df
    full_df = pd.DataFrame.from_dict(full_dict, orient='index')

    full_df.reset_index(inplace=True)
    full_df = full_df.rename(columns = {'index':'playerCode'})
    save_df_to_csv(full_df, filename, col_headers=True, index=True,
               index_label='idNum', mode='w')

    return full_df
