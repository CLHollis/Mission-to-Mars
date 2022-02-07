# SCRAPE MARS DATA - THE NEWS (latest article's title & summary) ........  Mod 10.3.3
#    Automate visiting a website & scrape ^

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# 10.5.3... Add Function to: 1) Initialize the browser. 2) Create a data dictionary.
#           3) End the WebDriver and return the scraped data
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # False = don't need to watch the script work anymore

    # The old setup from 10.3.3:  Set up an instance of a Splinter browser
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)  
    
    # set our news title and paragraph variables (remember, this function will return two values
    news_title, news_paragraph = mars_news(browser)
    hemispheres_image_urls = mars_hemispheres(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres_image_urls,
        "last_modified": dt.datetime.now()
        # adding the date the code was run last 
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # browser = we'll be using the browser variable we defined outside the function

    # Visit the website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')

        # Assign the title and summary text to variables we'll reference later
        #slide_elem.find('div', class_='content_title')
            
        # Use the parent element to find the first `a` tag & save it as news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title  ...move to return statement doesn't print within the function
            
        # Get the same thing, but Summary instead of Title
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p   ...move to return statement doesn't print within the function

    except AttributeError:
        return None, None

    return news_title, news_p
    # tells Python that the function is complete...the function can be executed, 
    #   and the result will be returned to the developer.





# SCRAPE MARS DATA - FEATURED IMAGE  .....................................  Mod 10.3.4
#    Always pull the full-size featured image. Automate: 
#    visiting a website, navigating through it, finding the 
#    full-size image, extract a link based on page location.

# Declare and define our function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()                          
        
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None

    # Add the base URL to create an full URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url

    return img_url




# SCRAPE MARS DATA - MARS FACTS (the table) ............................  Mod 10.3.5

# Visit URL
# url = 'https://galaxyfacts-mars.com/'
# browser.visit(url)

# At the top of your Jupyter Notebook, add import pandas as pd

def mars_facts():

    try:

        # Scrape the entire table with Pandas' .read_html() function
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        #df.head()

    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

    # Convert table to HTML, add bootstrap
    return df.to_html(classes="table table-striped")



# MARS Hemispheres Pics & pic titles

def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemispheres_image_urls = []
    
    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # loop through to get 4 different images
    for i in range(4):
    
        # Create empty dictionary
        hemispheres = {}
        
        # click on each hemisphere link
        browser.find_by_css('h3')[i].click()
        
        # navigate to the full-resolution image page
        # retrieve the full-resolution image URL string 
        img_url = browser.links.find_by_text('Sample').first['href']
        
        # retrieve the title for the hemisphere image 
        title = browser.find_by_css('h2.title').text

        # Save the full-res image URL string in "img_url" key that will be stored in the dictionary
        hemispheres["img_url"] = img_url
        # Save the hemisphere title in "title" key that will be stored in the dictionary
        hemispheres["title"] = title    
        # add the dictionary with the image URL string and the hemisphere image title to the list
        hemispheres_image_urls.append(hemispheres)
        
        # use browser.back() to navigate back to the beginning to get the next hemisphere image
        browser.back()

    return hemispheres_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

