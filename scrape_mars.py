import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape ():
    
    browser = init_browser()
    nasa_data = {}

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    nasa_data["nasa_headline"] = nasa_soup.find("div", class_="content-title").get_text()
    nasa_data["nasa_teaser"] = nasa_soup.find("div", class_="article-teaser-body").get_text()

    return nasa_data

def scrape ():

    browser = init_browser()
    jpl_data = {}

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')
    try:
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()

        img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
        image_path = f'https://www.jpl.nasa.gov{img_relative}'
        jpl_data["feature_image_src"] = image_path
    except ElementNotVisibleException:
        image_path = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22076_hires.jpg'
        jpl_data["feature_image_src"] = image_path

    return jpl_data

def scrape ():

    browser = init_browser()
    twitter_data = {}
        
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    twitter_data["weather_summary"] = mars_weather

    return twitter_data

def scrape ():

    browser = init_browser()
    facts_data = {}

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_facts_html = browser.html
    mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')

    fact_table = mars_facts_soup.find('table', class_='tablepress tablepress-id-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)
        
    for row in column2:
        value = row.text.strip()
        values.append(value)
        
    mars_facts = pd.DataFrame({
        "Facet":facets,
        "Value":values
        })

    mars_facts_html = mars_facts.to_html(header=False, index=False)
    facts_data["fact_table"] = mars_facts_html

    return facts_data

def scrape ():

    browser = init_browser()
    hemisphere_data = {}

    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        hemi_dict['title'] = hemi_name.strip()       
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

    hemishphere_data["hemisphere_imgs"] = hemi_dicts

    return hemishphere_data