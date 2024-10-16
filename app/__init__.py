from flask import Flask

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'secret key'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config['JSON_AS_ASCII'] = False #日本語を利用

  # blueprint登録
  from .routes import bp
  app.register_blueprint(bp)
  
  # データベース初期化
  from .models import db
  db.init_app(app)
  
  return app

