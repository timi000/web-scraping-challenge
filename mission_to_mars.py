from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #for mac users
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)




def space_image(browser):
        url2="https://www.jpl.nasa.gov/spaceimages/"
        browser.visit(url2)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('article', class_='carousel_item')["style"].split("'")[1]
        featured_image_url="http://www.jpl.nasa.gov"+img_url
        browser.quit()
        return featured_image_url

def image_dict(browser):
    astro_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)
    head_url=astro_url.split("search")[0]
    time.sleep(1)
    html = browser.html
    soup_ast=BeautifulSoup(html, "html.parser")
    hemisphere_images_url =[]
    hemp_list=soup_ast.find_all('div', class_="item")
    for hemp in hemp_list:
        try:
            title= hemp.find('h3').text
            hem_imp= hemp.img["src"]
            image=head_url+img_url
            if (title and image):
                post = {
                'titles': title,
                'image_url': image
                  }
                print(title)
                print(image)
            hemisphere_images_url.append(post)
        except Exception as e:
                print ("")
   
    return hemisphere_images_url



def new_info(browser): 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_article = soup.find_all('div', class_='content_title')[1].a.text
    news_p=soup.find('div', class_='article_teaser_body').text


    browser.quit()
    return news_article, news_p

def scrape_info(): 
    browser =init_browser()
    space_ig= space_image(browser)
    image_dic=image_dict(browser)
    news=new_info(browser)
   
   
    mars_data = {
                'news_title': news[0],
                'news_p': news[1],
                 'hemisphere': image_dic,
                 'feature_image_url': space_ig
                  }
    
    browser.quit()
    return mars_data



            









