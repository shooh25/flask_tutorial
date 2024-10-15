from flask import Flask
from .models import db

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'secret key'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config['JSON_AS_ASCII'] = False #日本語を利用

  db.init_app(app)
  return app
