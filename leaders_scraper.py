#%%timeit
import requests
#from functools import *
from bs4 import BeautifulSoup
import json
import re
import sys

root_url = "https://country-leaders.herokuapp.com"
country_url = "/countries"
cookie_url = "/cookie"
leaders_url = "/leaders"
status_url = "/status"
leaders_dic = {}
cache = {}

compiled = re.compile(r'<[^>]+>')
session= requests.Session()

#decorator for caching session
def hashable_cache(f):
    def inner(url, session):
        if url not in cache:
            cache[url] = f(url, session)
        return cache[url]
    return inner


def check_status():
    request = session.get(f"{root_url}{status_url}")
    if request.status_code == 200:
        print(request.text)
    else:
        sys.exit(request.status_code)
    
def create_cookies():
    cookies = session.get(f"{root_url}{cookie_url}")
    print(cookies.content)
    return cookies
 
def get_leaders():
    check_status()
    cookies = create_cookies()
    countries = session.get(f"{root_url}{country_url}",cookies = cookies.cookies)
    print("The list of countries", countries.json())
    
    for country in countries.json():
        leaders  = session.get(f"{root_url}{leaders_url}", cookies = cookies.cookies, params ={"country":country})
        # check if cookies is valid and create if it is missing
        if leaders.status_code!= 200:
            cookies = create_cookies()
            leaders  = session.get(f"{root_url}{leaders_url}", cookies = cookies.cookies, params ={"country":country})
        leaders_dic[country] = leaders.json()
    #create a Session object outside of the loop over countries.
    
    
    for country in leaders_dic:
        for leader in leaders_dic[country]:
            wikipedia_url= leader['wikipedia_url']
            if len(wikipedia_url) == 0:continue
            leader['paragraph'] = get_first_paragraph(wikipedia_url,session)
            
    save(leaders_dic)        
    #return leaders_dic
    
@hashable_cache         
def get_first_paragraph(wikipedia_url,session):
    print(wikipedia_url)
    leader_content = session.get(wikipedia_url).content
    soup = BeautifulSoup(leader_content, "html")
    paragraphs = soup.find_all("p")
    for paragraph in paragraphs:
        if str(paragraph)[3:6] =="<b>":
            string = str(paragraph)
            break
    # use regex to clean the paragraph
    first_paragraph = compiled.sub('',string)       
    return first_paragraph


def save(leaders_per_country):
    with open('leader.json', 'w') as fp:
        json.dump(leaders_per_country, fp)
        
    with open('leader.json', 'r') as fp:
        leader_data = json.load(fp)
    print(leader_data)
    


get_leaders()