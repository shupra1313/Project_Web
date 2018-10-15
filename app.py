from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

#use flask_pymongo to setup mongo DB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scrape"
mongo = PyMongo(app) 

@app.route('/')
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scraper():
    mars_data = mongo.db.mars_data
    mars_full_data = mars_scrape.scrape()
    mars_data.update({},mars_full_data, upsert=True)
    return redirect ("/", ) 

if __name__ == '__main__':
    app.run(debug=True)