from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def get_url(search_term):
    temp = 'https://www.hackerrank.com/{}?hr_r=1'
    search_term = search_term.replace(' ','+')
    return temp.format(search_term)

def main(search_term):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = get_url(search_term)
    driver.get(url)
    global userdata
    records = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    badges = soup.find_all('text',{'class':'badge-title'})
    fname = soup.find('h1',{'class':'profile-heading'}).text
    
    badges_list = list()
    for badge in badges:
        badges_list.append(badge.text[:])

    stars = soup.find_all('g',{'class': 'star-section'})
    stars_list = list()
    for star in stars:
        star = str(star)
        count = re.findall('class="badge-star"',star)
        stars_list.append(len(count))

    badge_stars = {}
    for i,j in zip(badges_list,stars_list):
        badge_stars.update({i:j})

    badge_stars = str(badge_stars)[1:-1]
    userdata.append((search_term,fname,badge_stars))

    driver.close()
    

users = pd.read_csv('users.csv')
userdata = []
for user in users.username:
    main(user)
    result = pd.DataFrame(userdata, columns=['Username','Fullname',"Badges"])

print(result)
result.to_csv('UserData.csv')
result.to_html('UserData.html')