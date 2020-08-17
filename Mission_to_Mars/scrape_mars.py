# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from splinter import Browser
import re
import time

def init_browser():
    executable_path = {'executable_path': 'driver/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # Mars News
    browser = init_browser()
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    news_article = soup.find_all('div', class_ = 'content_title')[1].a.text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    
    # Mars Image URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    pic_url = soup.find('div',class_='carousel_items').find('article','carousel_item')['style']
    pic_url_edit=re.search('\(([^)]+)', pic_url).group(1)
    featured_image_url='https://www.jpl.nasa.gov' + pic_url_edit.strip('"\'')
    
    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('div', class_='css-1dbjc4n r-aqfbo4 r-16y2uox').find('div',class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').find('span',class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text

    # Mars Facts
    mars_fact_url = 'https://space-facts.com/mars'
    tables = pd.read_html(mars_fact_url)
    fact_df = tables[0]
    html_table = fact_df.to_html()
    
    # Mars Hemispheres Image and Url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div',class_='item')
    hemisphere_image_urls=[]

    for result in results:
        a = result.find('a', class_="itemLink product-item")
        link = a['href']
        link_update = 'https://astrogeology.usgs.gov' + link
        browser.visit(link_update)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        html_sub = soup.find('div', class_='downloads')
        img = html_sub.find('a')
        img_url = img['href']
        title = soup.find('h2', class_='title').text
        hemisphere_dict = {'title':title, 'img_url':img_url}
        hemisphere_image_urls.append(hemisphere_dict)
    
    browser.quit()
    
    # Summary
    mars_summary = {"news_article":news_article, "news_p":news_p, "featured_image_url": featured_image_url,
                   "mars_weather": mars_weather, "mars_facts": html_table, "mars_Hemispheres": hemisphere_image_urls}

    return mars_summary