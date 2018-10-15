from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # define a path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    # creating an instance of the Browser module
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

     ####### Extract the latest title and the paragraph from the webpage #######

    
    #url of the page that is to be scraped
    url = "https://mars.nasa.gov/news/"
    # give the browser the url to be visited 
    browser.visit(url)

    html = browser.html
    # Give the html string to be parsed and also the corresponding parser and assign the url string to a variable 'soup'
    soup = BeautifulSoup(html,'html.parser')    

    news_title = soup.find('div', class_="content_title").text
    mars_data['news_title'] = news_title
    news_paragraph = soup.find('div', class_="article_teaser_body")
    mars_data['news_paragraph'] = news_paragraph

    ############ JPL Mars Space Images - Featured Image ############

    #url of the page to be scraped
    spaceimage_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #Getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(spaceimage_url))
    # give the browser the url to be visited 
    browser.visit(spaceimage_url)
    time.sleep(2)
    browser.find_by_id('full_image').click()
    # Then the html of that particular path is assigned to a variable 'html'
    html = browser.html
    # Give the html string to be parsed and the corresponding parser and then assign the url string to a variable 'soup'
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(2)
    # extract the image url for the current featured mars image and assign the url string to a variable called featured_image_url
    image_url = soup.find('img', class_ = 'fancybox-image')['src']
    featured_image_url = (base_url + image_url)
    mars_data["featured_image_url"] = featured_image_url


    ########################## Mars Weather #####################
    #url of the page that is to be scraped
    weather_url = "https://twitter.com/marswxreport?lang=en"
    # give the browser the url to be visited 
    browser.visit(weather_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweets = soup.findAll("p", class_ = 'tweet-text')
    # loop through every tweet you grab (findAll)
    for tweet in tweets:
    # if the tweet contains "Sol" we know it is a tweet about weather
        if 'Sol' in tweet.text:
            latest_weather = tweet.text
            break
    mars_data["weather_tweet"] = latest_weather

    ###################### Mars Facts #######################
    
    
    # url of the page to be scraped
    fact_url = "http://space-facts.com/mars/"
    # reading the url to find all the tables
    tables = pd.read_html(fact_url)
    # Selecting the first table (planet profile) from the list of tables
    mars_table = tables[0]
    # Assigning names to the columns
    mars_table.columns = ["parameter", "Values"]
    # setting parameter as the index
    mars_table_final = mars_table.set_index("parameter")
    # converting the pandas DF to a table in html
    mars_html_table = mars_table_final.to_html(index =True, header =True)
    # replacing all the new line markers with an empty space
    mars_html_table = mars_html_table.replace('\n', '')
    mars_data["mars_html_table"] = mars_html_table


    ################ Mars Hemispheres #######################


    #url of the page that is to be scraped
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # give the browser the url to be visited 
    browser.visit(hemisphere_url)

    #Getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hemisphere_url))
    
    #Create an empty list to append the image urls and titles later
    hemisphere_img_urls = []

                        # Cerberus Hemisphere Image #

    # The browser object finds the image url by its xpath and clicks on it
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
    # on clicking, it takes the browser object to the cerberus enhanced image page and finds the 'Open' button and clicks it
    browser.click_link_by_text("Open")
    # Then the html is assigned another variable and BS is used to parse that particular html for the specific element and class
    image = browser.html
    soup = BeautifulSoup(image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    # the base url is concatenated with the image url to get the final url
    cerberus_img_url = base_url + cerberus_url
    #To find the title of the image
    cerberus_title = soup.find("h2",class_="title").text
    
    #It takes the browser object back to the original url
    browser.back()

                        
                        # Schiaparelli Hemisphere Image #

    # The browser object finds the image url by its xpath and clicks on it
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    # on clicking, it takes the browser object to the schiaparelli enhanced image page and finds the 'Open' button and clicks it
    browser.click_link_by_text("Open")
    # Then the html is assigned another variable and BS is used to parse that particular html for the specific element and class
    image = browser.html
    soup = BeautifulSoup(image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    # the base url is concatenated with the image url to get the final url
    schiaparelli_img_url = base_url + schiaparelli_url
    #To find the title of the image
    schiaparelli_title = soup.find("h2",class_="title").text

    #It takes the browser object back to the original url
    browser.back()

                        
                        # Syrtis Major Hemisphere Image #
    
    # The browser object finds the image url by its xpath and clicks on it
    browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[3]/a/img').click()
    # on clicking, it takes the browser object to the syrtis major enhanced image page and finds the 'Open' button and clicks it
    browser.click_link_by_text("Open")
    # Then the html is assigned another variable and BS is used to parse that particular html for the specific element and class
    image = browser.html
    soup = BeautifulSoup(image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
    # the base url is concatenated with the image url to get the final url
    syrtis_major_img_url = base_url + syrtis_major_url
    #To find the title of the image
    syrtis_major_title = soup.find("h2",class_="title").text

    #It takes the browser object back to the original url
    browser.back()


                         # Valles Marineris Hemisphere Image #

    # The browser object finds the image url by its xpath and clicks on it
    browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    # on clicking, it takes the browser object to the valles marineris enhanced image page and finds the 'Open' button and clicks it
    browser.click_link_by_text("Open")
    # Then the html is assigned another variable and BS is used to parse that particular html for the specific element and class
    image = browser.html
    soup = BeautifulSoup(image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
    # the base url is concatenated with the image url to get the final url
    valles_marineris_img_url = base_url + valles_marineris_url
    # To find the title of the image
    valles_marineris_title = soup.find("h2",class_="title").text

    # Append all the 4 titles and image urls to the hemisphere_urls list
    hemisphere_img_urls.append({"Title":cerberus_title, "image url": cerberus_img_url})
    hemisphere_img_urls.append({"Title":schiaparelli_title, "image url": schiaparelli_img_url})
    hemisphere_img_urls.append({"Title":syrtis_major_title, "image url": syrtis_major_img_url})
    hemisphere_img_urls.append({"Title":valles_marineris_title, "image url": valles_marineris_img_url})
    
    mars_data["hemisphere_img_urls"] = hemisphere_img_urls

    # Finally return all the results
    return mars_data
