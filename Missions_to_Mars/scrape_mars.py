#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install webdriver_manager
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Using splinter to initialize chrome browser driver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = { "executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=True)


# In[3]:


# NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.
# I am going to have this function return a list of news and title
def nasa_mars_news():
    browser = init_browser()
    results_list = []

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
     # take all the news and save them, at the end will return the latest one
    results = soup.find_all("div",class_="list_text")
    
    for r in results:
        try:
            title = r.find("div", class_="content_title").text
            description = r.find("div", class_="article_teaser_body").text
            latest_news = {
                "title": title,
                "description": description
            }
            results_list.append(latest_news)
        except AttributeError as error:
            print(error)
        browser.links.find_by_partial_text("Next") 
    # I will try to return the latest news which is the first in my list
    browser.quit()
    return results_list[0]



# In[4]:


# PL Mars Space Images - Featured Image

# Visit the url for JPL Featured Space Image here.

# Use splinter to navigate the site and find the image url for the current 
# Featured Mars Image and assign the url string to a variable called featured_image_url.

# Make sure to find the image url to the full size .jpg image.

# Make sure to save a complete url string for this image.
 
def mars_featured_image():
    browser = init_browser()
    image_url = ""

    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    try:
        results = soup.find_all("img",class_="headerimage fade-in")
        for r in results:
            temp_url = r["src"]
            # put the base link and the image link together
            # replace index.html with image link
            image_url = url.replace("index.html",temp_url)
    except AttributeError as error:
        print(error)
    browser.quit()
    return image_url


# In[5]:


# Mars Facts

# Visit the Mars Facts webpage here and use Pandas to scrape the table containing
# facts about the planet including Diameter, Mass, etc.

# Use Pandas to convert the data to a HTML table string.
def mars_facts():
    url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(url)
    table_df = facts_table[0]
    table_df.columns = ["Description","Mars"]
    table_df = table_df.set_index(["Description"])
    html_table = table_df.to_html()
    html_table = html_table.replace("\n","")
    return html_table


# In[26]:


# Mars Hemispheres

# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar’s hemispheres.

# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

# Save both the image url string for the full resolution hemisphere image,
# and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data
#using the keys img_url and title.

# Append the dictionary with the image url string and the hemisphere title to a list.
#This list will contain one dictionary for each hemisphere.

def mars_hemi():
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    url_schiaparelli = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    url_syrtis = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    url_valles = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"

    # Place hemisphere urls into a list to be easy to loop through them
    hem_list = [url_cerberus, url_schiaparelli, url_syrtis, url_valles]

    # set up the splinter
    browser = init_browser()
    hemi_img_list = []

    # Go through all hemisphere urls
    # and take the urls for images
    for u in hem_list:
        browser.visit(u)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        try:
        # results = soup.find_all("div", class_="wide-image-wrapper")
            results = soup.find_all("div", class_="wide-image-wrapper")
            for r in results:
                link = r.find("ul").a["href"]
                hemi_img_list.append(link)
        except AttributeError as error:
            print(error)

    # go to the base link , find the links pointing to the hemisphere images and take their description
    descr_list = []
    browser.visit(url)
    html = browser.html
    base_soup = BeautifulSoup(html, "html.parser")
    try:
        results = base_soup.find_all("a", class_="itemLink product-item")
        for r in results:
            img = r.h3
            if img:
                img = img.text.strip("<h3>").strip("</h3>")
                descr_list.append(img)
    except AttributeError as error:
        print(error)
        
    # place the dictionares in this list    
    hemisphere_image_urls = []
    for d, u in zip(descr_list, hemi_img_list):
        item_dict = {"title": d, "img_url": u}
        hemisphere_image_urls.append(item_dict)
    return hemisphere_image_urls

# this function will execute all the code above in place the results into a dictionary
def scrape():
    mars_collections = {
        "news": nasa_mars_news(),
        "image": mars_featured_image(),
        "facts": mars_facts(),
        "hemisphere": mars_hemi()
    }
    return mars_collections


if __name__ in "__main__":
    results = scrape()
    print(results)