# -*- coding: utf-8 -*-
"""
NFL Stats Scraper

Author: Federico Scivittaro
Last Updated: 1/25/18

Description
"""

import random
import time
import pandas as pd

from util import get_soup
from util import save_df_to_csv
from manage_stats import get_season_stats_for_url_list
from manage_stats import append_market_share_data

BASE_URL = 'https://www.pro-football-reference.com'


def get_all_nfl_teams(year):
    """
    Get all NFL teams and links to their season stats for a given year.
    """
    
    url = BASE_URL + '/years/{}/'.format(year)
    soup = get_soup(url)
    
    table = soup.find('table', attrs={'id':'team_stats'})
    rows = table.find_all('tr')
    
    team_list = []
    
    for row in rows:
        team = row.find('td', attrs={'data-stat':'team'})
        
        if not team:
            continue
        
        team_link = team.find('a')
        
        if not team_link:
            continue
        
        team_link = team_link.get('href')
        team_list.append(team_link)
        
    return team_list


def get_all_nfl_teams_for_year_range(start_year, end_year):
    """
    Get all FBS teams and link to their season stats for a range of years.
    """
    
    full_team_list = []
    
    for year in range(start_year, end_year + 1):
        print(year)
        
        team_list = get_all_nfl_teams(year)
        full_team_list += team_list
        
        wait_time = random.randint(3, 15)
        time.sleep(wait_time)
    
    return full_team_list


def get_nfl_season_stats(url):
    """
    """
    
    full_url = BASE_URL + url
    print(full_url)
    soup = get_soup(full_url)
    
    header = soup.find('h1')
    spans = header.find_all('span')
    year = int(spans[0].get_text())
    team = spans[1].get_text()
    
    passing = soup.find('table', attrs={'id':'passing'})
    rush_rec = soup.find('table', attrs={'id':'rushing_and_receiving'})
    defense = soup.find('table', attrs={'id': 'defense'})
    
    rows_passing = passing.find_all('tr')[1:]
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
        player_id = player_stats_page[11:-4]
        player_year_id = player_id + '-' + str(year)
        
        age = int(row.find('td', attrs={'data-stat':'age'}).get_text())
        gp = int(row.find('td', attrs={'data-stat':'g'}).get_text())
        gs = int(row.find('td', attrs={'data-stat':'gs'}).get_text())

        cmp = row.find('td', attrs={'data-stat':'pass_cmp'}).get_text()

        if cmp:
            cmp = int(cmp)
        else:
            cmp = 0

        passatt = row.find('td', attrs={'data-stat':'pass_att'}).get_text()

        if passatt:
            passatt = int(passatt)
        else:
            passatt = 0

        pass_yds = row.find('td', attrs={'data-stat':'pass_yds'}).get_text()

        if pass_yds:
            pass_yds = int(pass_yds)
        else:
            pass_yds = 0

        passtd = row.find('td', attrs={'data-stat':'pass_td'}).get_text()

        if passtd:
            passtd = int(passtd)
        else:
            passtd = 0

        passint = row.find('td', attrs={'data-stat':'pass_int'}).get_text()

        if passint:
            passint = int(passint)
        else:
            passint = 0

        pass_ypa = row.find('td', attrs={'data-stat':'pass_yds_per_att'}).get_text()

        if pass_ypa:
            pass_ypa = float(pass_ypa)
        else:
            pass_ypa = 0

        pass_adj_ypa = row.find('td', attrs={'data-stat':'pass_adj_yds_per_att'}).get_text()

        if pass_adj_ypa:
            pass_adj_ypa = float(pass_adj_ypa)
        else:
            pass_adj_ypa = 0

        pass_rtg = row.find('td', attrs={'data-stat':'pass_rating'}).get_text()

        if pass_rtg:
            pass_rtg = float(pass_rtg)
        else:
            pass_rtg = 0

        pass_any_a = row.find('td', attrs={'data-stat':'pass_adj_net_yds_per_att'}).get_text()

        if pass_any_a:
            pass_any_a = float(pass_any_a)
        else:
            pass_any_a = 0

        sacks = row.find('td', attrs={'data-stat':'pass_sacked'}).get_text()

        if sacks:
            sacks = int(sacks)
        else:
            sacks = 0

        sack_pct = row.find('td', attrs={'data-stat':'pass_sacked_perc'}).get_text()

        if sack_pct:
            sack_pct = float(sack_pct)
        else:
            sack_pct = 0

        if passatt != 0:
            cmp_pct = round(cmp / passatt * 100, 1)
            td_pct = round(passtd / passatt * 100, 2)
            int_pct = round(passint / passatt * 100, 2)
        else:
            cmp_pct = 0
            td_pct = 0
            int_pct = 0
        
        passing_dict[player_year_id] = {'Name': name,
                                        'Team': team,
                                        'Year': year,
                                        'Age': age,
                                        'GP': gp,
                                        'GS': gs,
                                        'CMP': cmp,
                                        'ATT': passatt,
                                        'CMP PCT': cmp_pct,
                                        'YARDS': pass_yds,
                                        'YPA': pass_ypa,
                                        'ADJ YPA': pass_adj_ypa,
                                        'TD': passtd,
                                        'INT': passint,
                                        'SACK': sacks,
                                        'PASS RTG': pass_rtg,
                                        'PASS ANY/A': pass_any_a,
                                        'TD PCT': td_pct,
                                        'INT PCT': int_pct,
                                        'SACK PCT': sack_pct,
                                        'Player ID': player_id,
                                        'Link': player_stats_page}
        
    for row in rows_rush_rec:
        a = row.find('a')
        
        if not a:
            continue
        
        name = a.get_text()
        player_stats_page = a.get('href')
        player_id = player_stats_page[11:-4]
        player_year_id = player_id + '-' + str(year)
        
        age = int(row.find('td', attrs={'data-stat':'age'}).get_text())
        gp = int(row.find('td', attrs={'data-stat':'g'}).get_text())
        gs = int(row.find('td', attrs={'data-stat':'gs'}).get_text())

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
        
        tgt = row.find('td', attrs={'data-stat':'targets'}).get_text()

        if tgt:
            tgt = int(tgt)
        else:
            tgt = 0

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

        fmb = row.find('td', attrs={'data-stat':'fumbles'}).get_text()

        if fmb:
            fmb = int(fmb)
        else:
            fmb = 0

        if tgt != 0:
            catch_pct = round(rec / tgt * 100, 1)
        else:
            catch_pct = 0
        
        rush_rec_dict[player_year_id] = {'Name': name,
                                         'Team': team,
                                         'Year': year,
                                         'Age': age,
                                         'GP': gp,
                                         'GS': gs,
                                         'RUSH ATT': rushatt,
                                         'RUSH YDS': rushyds,
                                         'RUSH YPA': rushypa,
                                         'RUSH TD': rushtd,
                                         'TGT': tgt,
                                         'REC': rec,
                                         'CATCH PCT': catch_pct,
                                         'REC YDS': recyds,
                                         'REC YPC': recypc,
                                         'REC TD': rectd,
                                         'FMB': fmb,
                                         'Player ID': player_id,
                                         'Link': player_stats_page}
    
    for row in rows_defense:
        a = row.find('a')
        
        if not a:
            continue
        
        name = a.get_text()
        player_stats_page = a.get('href')
        player_id = player_stats_page[11:-4]
        player_year_id = player_id + '-' + str(year)
        
        age = int(row.find('td', attrs={'data-stat':'age'}).get_text())
        gp = int(row.find('td', attrs={'data-stat':'g'}).get_text())
        gs = int(row.find('td', attrs={'data-stat':'gs'}).get_text())

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

        qb_hit = row.find('td', attrs={'data-stat':'qb_hits'}).get_text()

        if qb_hit:
            qb_hit = int(qb_hit)
        else:
            qb_hit = 0
        
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
                                        'Age': age,
                                        'GP': gp,
                                        'GS': gs,
                                        'SOLO TCKL': solo_tckl,
                                        'TFL': tfl,
                                        'SACK': sacks,
                                        'HIT': qb_hit,
                                        'INT': def_int,
                                        'PBU': pbu,
                                        'FF': ff,
                                        'Player ID': player_id,
                                        'Link': player_stats_page}
        
    return passing_dict, rush_rec_dict, defense_dict


def nfl_job():
    """
    """
    
    start_year = 2000
    end_year = 2009
    
    url_list = get_all_nfl_teams_for_year_range(start_year, end_year)
    
    d1, d2, d3 = get_season_stats_for_url_list(url_list, get_nfl_season_stats)
    
    df1 = pd.DataFrame.from_dict(d1, orient='index')
    df2 = pd.DataFrame.from_dict(d2, orient='index')
    df3 = pd.DataFrame.from_dict(d3, orient='index')
    
    save_df_to_csv(df1, 'Data/NFL/passing.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    save_df_to_csv(df2, 'Data/NFL/rush_receiving.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    save_df_to_csv(df3, 'Data/NFL/defense.csv', col_headers=False, index=True,
                   index_label='PlayerYearID', mode='a')
    
    rush_rec_stats_list = ['RUSH ATT', 'RUSH YDS', 'RUSH TD', 'REC', 'REC YDS', 'REC TD']
    rush_rec_shares = append_market_share_data('Data/NFL/rush_receiving.csv', rush_rec_stats_list)
    
    def_stats_list = ['SOLO TCKL', 'TFL', 'SACK', 'INT', 'PBU', 'FF']
    def_shares = append_market_share_data('Data/NFL/defense.csv', def_stats_list)
    
    return df1, df2, df3, rush_rec_shares, def_shares