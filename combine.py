# -*- coding: utf-8 -*-
"""
NFL Draft Combine Scraper

Author: Federico Scivittaro
Last Updated: 12/12/18

Description
"""

import random
import time
import pandas as pd

from util import get_soup
from util import save_df_to_csv
from util import open_csv_to_df

BASE_URL = 'https://www.pro-football-reference.com'

def scrape_combine_results(year):
    """
    """
    
    url = BASE_URL + '/draft/{}-combine.htm'.format(year)
    soup = get_soup(url)
    
    table = soup.find('table', attrs={'id': 'combine'})
    rows = table.find_all('tr')
    
    data_dict = {}
    
    for row in rows:
        th = row.find('th', attrs={'data-stat':'player'})
        name = th.get_text().strip()
        
        if name == 'Player':
            continue
        
        a_tag = th.a
        
        if a_tag:
            nfl_stats = a_tag.get('href')
            nfl_id = nfl_stats[11:-4]
        else:
            nfl_stats = None
            nfl_id = None
        
        pos = row.find('td', attrs={'data-stat':'pos'}).get_text().strip()
        team = row.find('td', attrs={'data-stat':'school_name'}).get_text().strip()
        
        is_link = row.find('td', attrs={'data-stat':'college'}).a
        
        if is_link:
            college_stats = is_link.get('href')[32:]
            college_id = college_stats[13:-5]
            player_id = college_id
        else:
            college_stats = None
            college_id = None
            player_id = name.lower().replace(' ', '-') + '-' + str(year)
        
        height_old = row.find('td', attrs={'data-stat':'height'}).get_text()
        
        if height_old:
            height_list = height_old.split('-')
            feet = int(height_list[0])
            inches = int(height_list[1])
            height = (feet * 12) + inches
        else:
            height = None
        
        
        def find_attr(instance):
            """
            Find the data-stat in the row that has the desired instance;
            get_text if applicable, else return the NoneType.
            """
            
            val = row.find('td', attrs={'data-stat':instance})
            
            if val:
                val = val.get_text()
            else:
                val = None
            
            return val
        
        
        weight = find_attr('weight')
        forty = find_attr('forty_yd')
        vert = find_attr('vertical')
        bench = find_attr('bench_reps')        
        broad = find_attr('broad_jump')
        cone = find_attr('cone')
        shuttle = find_attr('shuttle')
        
        data_dict[player_id] = {'Name': name,
                                'Year': year,
                                'POS': pos,
                                'Team': team,
                                'HGT': height,
                                'WGT': weight,
                                'FORTY': forty,
                                'VERT': vert,
                                'BENCH': bench,
                                'BROAD': broad,
                                'CONE': cone,
                                'SHUT': shuttle,
                                'College Link': college_stats,
                                'NFL Link': nfl_stats,
                                'CollegeID': college_id,
                                'PlayerID': nfl_id}

    return data_dict


def scrape_combine_data_for_year_range(start_year, end_year):
    """
    """
    
    full_dict = {}
    
    for year in range(start_year, end_year + 1):
        print(year)
        year_dict = scrape_combine_results(year)
        full_dict.update(year_dict)
    
        wait_time = random.randint(15, 60)
        time.sleep(wait_time)
    
    return full_dict


def job():
    """
    """
    
    start_year = 2019
    end_year = 2019
    
    data_dict = scrape_combine_data_for_year_range(start_year, end_year)
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    
    save_df_to_csv(df, 'Data/combine.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    
    return df