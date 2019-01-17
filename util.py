# -*- coding: utf-8 -*-
"""
Data Management Utilities

Author: Federico Scivittaro

Date: 6/28/17

Contains utility functions applicable to all files. Functions are responsible
for making requests to a server and for performing basic data storage and
management.
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ConnectionError, Timeout

from bs4 import BeautifulSoup
import time
import pandas as pd
import re

def prepare_request(num_retries=100, timeout=3.1):
    """
    Returns a prepared request with mounted retry and timeout parameters. The
    request will try to access the server num_retries times before returning an
    exception and will timeout after timeout seconds (by convention timeout is
    set to slightly larger than a multiple of 3). A timeout will prompt a
    retry.
    """

    req = requests.Session()

    retries = Retry(total = num_retries,
                    backoff_factor = 10, # Delay of 10 seconds
                    status_forcelist = [500, 502, 503, 504])

    req.mount('http://', HTTPAdapter(max_retries = retries)) # Mount the retry
    req.mount('https://', HTTPAdapter(max_retries = retries))
    
    # Create class capable of mounting timeouts
    class TimeoutAdapter(HTTPAdapter):
        def __init__(self, timeout=None, *args, **kwargs):
            self.timeout = timeout
            super(TimeoutAdapter, self).__init__(*args, **kwargs)
            
        def send(self, *args, **kwargs):
            kwargs['timeout'] = self.timeout
            return super(TimeoutAdapter, self).send(*args, **kwargs)
        
        
    req.mount('http://', TimeoutAdapter(timeout=timeout)) # Mount the timeout
    req.mount('https://', TimeoutAdapter(timeout=timeout))

    return req


def make_robust_request(url, num_retries=100, timeout=3.1, headers=None,
                        params=None):
    """
    Tries to send a request and return a response from the server. Will sleep
    for 60 seconds and then try again (up to ten times) in the case of a
    Connection Error or Read Timeout error.
    """
    
    req = prepare_request(num_retries, timeout)
    attempts = 0
    
    while attempts < num_retries: # Max attempts before failing
        try:
            r = req.get(url, headers=headers, params=params)
            break
        except (ConnectionError, Timeout) as error:
            print(str(error) + ' -- waiting 60 seconds')
            attempts += 1
            time.sleep(60) # Give some time before trying again
        except:
            print('Unknown error -- waiting 60 seconds')
            attempts += 1
            time.sleep(60) # Give some time before trying again
    
    r.raise_for_status()
    
    return r


def get_soup(url, num_retries=100, timeout=3.1, headers=None, params=None):
    """
    Tries to send a BeautifulSoup request and return a response from the
    server. Will sleep for 60 seconds and then try again (up to ten times) in
    the case of a Connection Error or Read Timeout error.
    """
    
    req = prepare_request(num_retries, timeout)
    
    attempts = 0
    
    while attempts < 100: # Max of 100 attempts before failing
        try:
            r = req.get(url, headers=headers, params=params)
            r.raise_for_status()      
            
            r2 = re.sub(r'<!--', '', r.text)
            r3 = re.sub(r'-->', '', r2)
            soup = BeautifulSoup(r3, 'lxml')
            break
        
        except (ConnectionError, Timeout) as error:
            print(str(error) + ' -- waiting 60 seconds')
            attempts += 1
            time.sleep(60) # Give some time before trying again
            
        except:
            print('Unknown error -- waiting 60 seconds')
            attempts += 1
            time.sleep(60) # Give some time before trying again
    
    return soup


def save_df_to_csv(df, filename, col_headers=True, index=False,
                   index_label=None, mode='a'):
    """
    Saves the df to a csv file.
    """
    
    if not df.empty:
        df.to_csv(filename, sep='|', header=col_headers, index=index,
                  index_label=index_label, mode=mode, encoding='utf-8')
    
    return None


def open_csv_to_df(filename, index=None):
    """
    Loads a CSV file and returns it as a Pandas df.
    """
    
    df = pd.read_csv(filename, sep='|', header=0, index_col=index, 
                     encoding='utf-8')
    
    return df

