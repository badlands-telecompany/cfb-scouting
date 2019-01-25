# -*- coding: utf-8 -*-
"""
College Stats Scraper

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

BASE_URL = 'https://www.sports-reference.com'


def get_all_fbs_teams(year):
    """
    Get all FBS teams and links to their season stats for a given year.
    """
    
    url = BASE_URL + '/cfb/years/{}-standings.html'.format(year)
    soup = get_soup(url)
    
    table = soup.find('table', attrs={'id':'standings'})
    rows = table.find_all('tr')
    
    team_list = []
    
    for row in rows:
        team = row.find('td', attrs={'data-stat':'school_name'})
        
        if not team:
            continue
        
        team_link = team.find('a').get('href')        
        team_list.append(team_link)
        
    return team_list


def get_all_fbs_teams_for_year_range(start_year, end_year):
    """
    Get all FBS teams and link to their season stats for a range of years.
    """
    
    full_team_list = []
    
    for year in range(start_year, end_year + 1):
        print(year)
        
        team_list = get_all_fbs_teams(year)
        full_team_list += team_list
        
        wait_time = random.randint(3, 15)
        time.sleep(wait_time)
    
    return full_team_list


def get_season_stats(url):
    """
    """
    
    full_url = BASE_URL + url
    soup = get_soup(full_url)
    
    header = soup.find('h1')
    spans = header.find_all('span')
    year = int(spans[0].get_text())
    team = spans[1].get_text()
    
    passing = soup.find('table', attrs={'id':'passing'})
    rush_rec = soup.find('table', attrs={'id':'rushing_and_receiving'})
    defense = soup.find('table', attrs={'id': 'defense_and_fumbles'})
    
    rows_passing = passing.find_all('tr')[2:]
    rows_rush_rec = rush_rec.find_all('tr')[2:]
    rows_defense = defense.find_all('tr')[2:]
    
    passing_dict = {}
    rush_rec_dict = {}
    defense_dict = {}
    
    for row in rows_passing:
        a = row.find('a')
        
        if not a:
            continue
        
        name = a.get_text()
        player_stats_page = a.get('href')
        player_id = player_stats_page[13:-5]
        player_year_id = player_id + '-' + str(year)
        
        cmp = int(row.find('td', attrs={'data-stat':'pass_cmp'}).get_text())
        passatt = int(row.find('td', attrs={'data-stat':'pass_att'}).get_text())
        cmp_pct = float(row.find('td', attrs={'data-stat':'pass_cmp_pct'}).get_text())
        pass_yds = int(row.find('td', attrs={'data-stat':'pass_yds'}).get_text())
        ypa = float(row.find('td', attrs={'data-stat':'pass_yds_per_att'}).get_text())
        adj_ypa = float(row.find('td', attrs={'data-stat':'adj_pass_yds_per_att'}).get_text())
        passtd = int(row.find('td', attrs={'data-stat':'pass_td'}).get_text())
        passint = int(row.find('td', attrs={'data-stat':'pass_int'}).get_text())
        pass_rtg = float(row.find('td', attrs={'data-stat':'pass_rating'}).get_text())
        
        td_pct = round(passtd / passatt * 100, 2)
        int_pct = round(passint / passatt * 100, 2)
        
        passing_dict[player_year_id] = {'Name': name,
                                        'Team': team,
                                        'Year': year,
                                        'CMP': cmp,
                                        'ATT': passatt,
                                        'CMP PCT': cmp_pct,
                                        'YARDS': pass_yds,
                                        'YPA': ypa,
                                        'ADJ YPA': adj_ypa,
                                        'TD': passtd,
                                        'INT': passint,
                                        'PASS RTG': pass_rtg,
                                        'TD PCT': td_pct,
                                        'INT PCT': int_pct,
                                        'Player ID': player_id,
                                        'Link': player_stats_page}
        
    for row in rows_rush_rec:
        a = row.find('a')
        
        if not a:
            continue
        
        name = a.get_text()
        player_stats_page = a.get('href')
        player_id = player_stats_page[13:-5]
        player_year_id = player_id + '-' + str(year)
        
        rushatt = row.find('td', attrs={'data-stat':'rush_att'}).get_text()
        
        if rushatt:
            rushatt = int(rushatt)
        else:
            rushatt = 0
    
        rushyds = row.find('td', attrs={'data-stat':'rush_yds'}).get_text()
        
        if rushyds:
            rushyds = int(rushyds)
        else:
            rushyds = 0
        
        rushypa = row.find('td', attrs={'data-stat':'rush_yds_per_att'}).get_text()
        
        if rushypa:
            rushypa = float(rushypa)
        else:
            rushypa = 0
        
        rushtd = row.find('td', attrs={'data-stat':'rush_td'}).get_text()
        
        if rushtd:
            rushtd = int(rushtd)
        else:
            rushtd = 0
        
        rec = row.find('td', attrs={'data-stat':'rec'}).get_text()
        
        if rec:
            rec = int(rec)
        else:
            rec = 0
        
        recyds = row.find('td', attrs={'data-stat':'rec_yds'}).get_text()
        
        if recyds:
            recyds = int(recyds)
        else:
            recyds = 0
        
        recypc = row.find('td', attrs={'data-stat':'rec_yds_per_rec'}).get_text()
        
        if recypc:
            recypc = float(recypc)
        else:
            recypc = 0
        
        rectd = row.find('td', attrs={'data-stat':'rec_td'}).get_text()
        
        if rectd:
            rectd = int(rectd)
        else:
            rectd = 0
        
        rush_rec_dict[player_year_id] = {'Name': name,
                                         'Team': team,
                                         'Year': year,
                                         'RUSH ATT': rushatt,
                                         'RUSH YDS': rushyds,
                                         'RUSH YPA': rushypa,
                                         'RUSH TD': rushtd,
                                         'REC': rec,
                                         'REC YDS': recyds,
                                         'REC YPC': recypc,
                                         'REC TD': rectd,
                                         'Player ID': player_id,
                                         'Link': player_stats_page}
    
    for row in rows_defense:
        a = row.find('a')
        
        if not a:
            continue
        
        name = a.get_text()
        player_stats_page = a.get('href')
        player_id = player_stats_page[13:-5]
        player_year_id = player_id + '-' + str(year)
        
        solo_tckl = row.find('td', attrs={'data-stat':'tackles_solo'}).get_text()
        
        if solo_tckl:
            solo_tckl = int(solo_tckl)
        else:
            solo_tckl = 0
        
        tfl = row.find('td', attrs={'data-stat':'tackles_loss'}).get_text()
        
        if tfl:
            tfl = float(tfl)
        else:
            tfl = 0        
        
        sacks = row.find('td', attrs={'data-stat':'sacks'}).get_text()
        
        if sacks:
            sacks = float(sacks)
        else:
            sacks = 0        
        
        def_int = row.find('td', attrs={'data-stat':'def_int'}).get_text()
        
        if def_int:
            def_int = int(def_int)
        else:
            def_int = 0        
        
        pbu = row.find('td', attrs={'data-stat':'pass_defended'}).get_text()
        
        if pbu:
            pbu = int(pbu)
        else:
            pbu = 0        
        
        ff = row.find('td', attrs={'data-stat':'fumbles_forced'}).get_text()
        
        if ff:
            ff = int(ff)
        else:
            ff = 0        
        
        defense_dict[player_year_id] = {'Name': name,
                                        'Team': team,
                                        'Year': year,
                                        'SOLO TCKL': solo_tckl,
                                        'TFL': tfl,
                                        'SACK': sacks,
                                        'INT': def_int,
                                        'PBU': pbu,
                                        'FF': ff,
                                        'Player ID': player_id,
                                        'Link': player_stats_page}
        
    return passing_dict, rush_rec_dict, defense_dict


def get_season_stats_for_url_list(url_list):
    """
    """
    
    full_pass_dict = {}
    full_rush_rec_dict = {}
    full_defense_dict = {}
    
    i = 1
    
    for url in url_list:
        d1, d2, d3 = get_season_stats(url)
    
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


def job():
    """
    """
    
    start_year = 2018
    end_year = 2018
    
    url_list = get_all_fbs_teams_for_year_range(start_year, end_year)
    
    d1, d2, d3 = get_season_stats_for_url_list(url_list)
    
    df1 = pd.DataFrame.from_dict(d1, orient='index')
    df2 = pd.DataFrame.from_dict(d2, orient='index')
    df3 = pd.DataFrame.from_dict(d3, orient='index')
    
    save_df_to_csv(df1, 'Data/passing.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    save_df_to_csv(df2, 'Data/rush_receiving.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    save_df_to_csv(df3, 'Data/defense.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    
    rush_rec_stats_list = ['RUSH ATT', 'RUSH YDS', 'RUSH TD', 'REC', 'REC YDS', 'REC TD']
    rush_rec_shares = append_market_share_data('Data/rush_receiving.csv', rush_rec_stats_list)
    
    def_stats_list = ['SOLO TCKL', 'TFL', 'SACK', 'INT', 'PBU', 'FF']
    def_shares = append_market_share_data('Data/defense.csv', def_stats_list)
    
    return df1, df2, df3, rush_rec_shares, def_shares