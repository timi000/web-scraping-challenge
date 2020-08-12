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


def scrape_info(): 
    browser =init_browser()
    time.sleep(10)
    image_dic=image_dict()
    news=new_info(browser)
    time.sleep(10)
    space_ig= space_image(browser)
    time.sleep(10)
    m_tweet=tweet(browser)
    time.sleep(10)
  
   
   
    mars_data = {'tweet':m_tweet,
                'news_title': news[0],
                'news_p': news[1],
                 'hemisphere': image_dic,
                 'feature_image_url': space_ig
                  }
    
    browser.quit()
    print (mars_data)
    return mars_data

def space_image(browser):
        url2="https://www.jpl.nasa.gov/spaceimages/"
        browser.visit(url2)
        time.sleep(10)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('article', class_='carousel_item')["style"].split("'")[1]
        featured_image_url="http://www.jpl.nasa.gov"+img_url
       
        return featured_image_url

def image_dict():
    astro_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response=requests.get(astro_url)
    print(response)
    head_url=astro_url.split("search")[0]
    soup_ast=BeautifulSoup(response.text, "html.parser")
    hemisphere_images_url =[]
    hemp_list=soup_ast.find_all('div', class_="item")
    for hemp in hemp_list:
        title= hemp.find('h3').text
        hem_imp= hemp.img["src"]
        image=head_url+hem_imp
        if (title and image):
            post = {
                'titles': title,
                'image_url': image
                 }
        hemisphere_images_url.append(post)
    print(hemisphere_images_url)

    return hemisphere_images_url


def new_info(browser): 
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_article = soup.find_all('div', class_='content_title')[1].a.text
    news_p=soup.find('div', class_='article_teaser_body').text
    

 
    return news_article, news_p
def tweet(browser): 
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    Tweet=weather_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    mars_tweet=Tweet[38].text

    
    

 
    return mars_tweet





            









