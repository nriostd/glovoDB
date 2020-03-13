from flask import Flask
from os import environ


app = Flask(__name__, instance_relative_config=True)
app.config["MONGO_URI"]= environ.get('MONGO_URI')
from app import views

#load the config file
app.config.from_object('config')
