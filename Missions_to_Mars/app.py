from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
#mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.marsDB

@app.route("/")
def index():
    mars_data = db.mars_collection.find_one()
    print(mars_data)
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    db = client.marsDB
    db = db.mars_collection
    mars_data = scrape()
  #  print(mars_data)
    db.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

# just a temporary function to place the data in mongoDB
def place_data():
    mars_collection = scrape()
    db = client.marsDB
    db = db.mars_collection
    db.insert_one(mars_collection)
    

if __name__ == "__main__":
    app.run(debug=True)
    place_data()