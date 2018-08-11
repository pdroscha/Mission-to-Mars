import time
import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

mission_to_mars = {}

def scrape ():
    
    browser = init_browser()

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    title = nasa_soup.find("div", class_="content-title").text()
    mission_to_mars["headline"] = title

    paragraph = nasa_soup.find("div", class_="article-teaser-body").text()
    mission_to_mars["article"] = paragraph
    print

    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    image_results = jpl_soup.find('img', class_='thumb')
    image_src = image_results['src']
    featured_image = 'https://www.jpl.nasa.gov/' + image_src

    mission_to_mars['featured_image'] = featured_image
    print
    
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(mars_weather_url)
    soup_tweet = BeautifulSoup(response.text,'html.parser')
    recent_tweet = soup_tweet.find('p',class_='TweetTextSize').text

    mission_to_mars['weather_tweet'] = recent_tweet
    print 

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)

    mars_table_df = mars_table[0]
    mars_table_df.columns = ['Fact','Values']

    mars_table_html = mars_table_df.to_html(header=True, index=False)
    mission_to_mars['mars_facts_table'] = mars_table_html
    print

    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)
    html = browser.html
    mars_soup = BeautifulSoup(html,'html.parser')
    hemisphere = mars_soup.find('div',class_='collapsible results')

    results = hemisphere.find('a')


    hemisphere_list = []

    for result in results:
        if result.h3:
            title = result.h3
            link = 'https://astrogeology.usgs.gov'
            print(title,link)    
            browser.visit(link)
            time.sleep(5)
            image_html = browser.html
            soup_scrape = BeautifulSoup(image_html,'html.parser') + result['href']
            soup_image = soup_scrape.find('div', class_='downloads').find('li').a['href']
            print(soup_image)
            mars_images = {'title':title, 'img_url':soup_image}
            hemisphere_list.append(mars_images)

            print(hemisphere_list)

            #Cerberus
            cerberus = hemisphere_list[0]['img_url']
            mission_to_mars['cerberus'] = cerberus
            #Shciaparelli
            schiaparelli = hemisphere_list[1]['img_url']
            mission_to_mars['schiaparelli'] = schiaparelli
            #Syrtis Major
            syrtis_major = hemisphere_list[2]['img_url']
            mission_to_mars['syrtis_major'] = syrtis_major
            #Valles Marineris
            valles_marineris = hemisphere_list[3]['img_url']
            mission_to_mars['valles_marineris'] = valles_marineris
    print

    return mission_to_mars