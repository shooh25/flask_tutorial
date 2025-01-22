from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
  __tablename__ = 'books'
  
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(256), nullable=False)
  title = db.Column(db.String(512), nullable=False)
  publisher = db.Column(db.String(256), nullable=True)
  price = db.Column(db.Integer, nullable=True)
  isbn = db.Column(db.String(10), nullable=False)

class Sample(db.Model):
  __tablename__ = 'sample'
  id = db.Column(db.String, primary_key=True)

# cur.execute("create table BOOKLIST(
# ID int primary key,
# AUTHOR varchar(256),
# TITLE varchar(512),
# PUBLISHER varchar(256),
# PRICE int,
# ISBN char(10))")
