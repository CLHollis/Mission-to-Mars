    # Import tools
from flask import Flask, render_template, redirect, url_for
    # use Flask to render a template, redirecting to another url, and creating a URL
from flask_pymongo import PyMongo
    # use PyMongo to interact with our Mongo database
import scraping
    # to use the scraping code, we will convert from Jupyter notebook to Python

    # Set up Flask
app = Flask(__name__)
    
    # Tell Python how to connect to Mongo using PyMongo
    # / Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
    # app.config["MONGO_URI"] = tells Python that our app will connect to Mongo 
    #   using a URI, a uniform resource identifier similar to a URL
    # "mongodb://localhost:27017/mars_app" = the URI we'll be using to connect 
    #   our app to Mongo. Literally... The app can reach Mongo through our localhost 
    #   server, using port 27017, using a database named "mars_app"
mongo = PyMongo(app)


# Define the route for the HTML page.
@app.route("/")
    # @app.route("/") = tells Flask what to display when we're looking at the home page, 
    #   index.html (index.html is the default HTML file that we'll use to display the 
    #   content we've scraped). This means that when we visit our web app's HTML page, 
    #   we will see the home page.

    # Function linking our visual representation of our work (our web app) to the code that powers it
def index():
   mars = mongo.db.mars.find_one()
        # assign that path to themars variable for use later
        # mars = mongo.db.mars.find_one() = uses PyMongo to find the "mars" collection 
        #   in our database, which we will create when we convert our Jupyter scraping 
        #   code to Python Script
   return render_template("index.html", mars=mars)
        # return render_template("index.html" = tells Flask to return an HTML template 
        #   using an index.html file. We'll create this file after we build the Flask routes.
        # , mars=mars) = tells Python to use the "mars" collection in MongoDB


# Set up our scraping route - the "button" of the web application
    #   the one that will scrape updated data when we tell it to from the homepage of our 
    #   web app. It'll be tied to a button that will run the code when it's clicked.
@app.route("/scrape")
    # @app.route(“/scrape”) defines the route that Flask will be using. 
    # “/scrape” = will run the function that we create just beneath it.

    # Function to 
    # 1. access the database, 
    # 2. scrape new data using our scraping.py script, 
    # 3. update the database, and 
    # 4. return a message when successful
def scrape():
    # define it
   mars = mongo.db.mars
        # assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all()
        # created a new variable to hold the newly scraped data
        # referencing the scrape_all function in the scraping.py file exported from JN
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #   .update_one(query_parameter, {"$set": data}, options)
        # mars.update_one() = Update the database...
        # inserting data, but not if an identical record already exists
        #   In the query_parameter, we can 
        #   1) specify a field (e.g. {"news_title": "Mars Landing Successful"}), in which 
        #       case MongoDB will update a document with a matching news_title. 
        #   2) Or it can be left empty ({}) to update the 1st matching doc in the collection.
        # {"$set": data} = use the data we have stored in mars_data
        # upsert=True = indicates to Mongo to create a new doc if one doesn't already exist
        #   & new data will always be saved (even if we haven't already created a doc for it)
   return redirect('/', code=302)
        # add a redirect after successfully scraping the data
        # This will navigate our page back to "/" where we can see the updated content.

# Tell it to run
if __name__ == "__main__":
   app.run(debug=True)