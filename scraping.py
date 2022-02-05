# SCRAPE MARS DATA - THE NEWS (latest article's title & summary) ........  Mod 10.3.3
#    Automate visiting a website & scrape ^

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set up an instance of a Splinter browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)  
    
# Visit the website
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

# Assign the title and summary text to variables we'll reference later
slide_elem.find('div', class_='content_title')
    
# Use the parent element to find the first `a` tag & save it as news_title
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
    
# Get the same thing, but Summary instead of Title
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# SCRAPE MARS DATA - FEATURED IMAGE  .....................................  Mod 10.3.4
#    Always pull the full-size featured image. Automate: 
#    visiting a website, navigating through it, finding the 
#    full-size image, extract a link based on page location.

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()                          
    
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Add the base URL to create an full URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url
    
# SCRAPE MARS DATA - MARS FACTS (the table) ............................  Mod 10.3.5

# Visit URL
url = 'https://galaxyfacts-mars.com/'
browser.visit(url)

# At the top of your Jupyter Notebook, add import pandas as pd

# Scrape the entire table with Pandas' .read_html() function
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

# Convert table to HTML
df.to_html()

# Close down the website (like turning off lights when leaving a room)
browser.quit()

