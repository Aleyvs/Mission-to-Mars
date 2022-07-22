
from flask import Flask, redirect, render_template, url_for
from flask_pymongo import PyMongo

import scraping

## setiup Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

## home page route with index function 
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()  # uses PyMongo to find the 'mars' collection in our db
   return render_template("index.html", mars=mars) # tells Flask to return a HTML template using the index.html file

## route to the scrape function
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   
   return redirect('/', code=302)

  
if __name__ == "__main__":
   app.run()
