from flask import Blueprint
from .models import Books

bp = Blueprint("bp", __name__)

@bp.route("/")
def index():
  return "Hello, World"

# 全ての書籍を取得
@bp.route("/books", methods=['GET'])
def get_all_books():
  
  books: list[Books] = Books.query.all()
  if books:
    return [
      {
        "id": book.id,
        "author": book.author,
        "title": book.title,
        "publisher": book.publisher,
        "price": book.price,
        "isbn": book.isbn,
      }
      for book in books
    ]
  return {"message": 'Not found'}, 404

# 指定したIDの書籍を取得
@bp.route("/books/<int:id>", methods=['GET'])
def get_book(id):
  book: Books = Books.query.get(id)
  if book:
    return {
      "id": book.id,
      "author": book.author,
      "title": book.title,
      "publisher": book.publisher,
      "price": book.price,
      "isbn": book.isbn, 
    }
  return {"message": 'Not found'}, 404

# タイトル検索
@bp.route("/search/<string:title>", methods=['GET'])
def search_book(title):
  books = Books.query.filter(Books.title.like(f'%{title}%')).all()
  if books:
    return [
      {
        "id": book.id,
        "author": book.author,
        "title": book.title,
        "publisher": book.publisher,
        "price": book.price,
        "isbn": book.isbn,
      }
      for book in books
    ]
  return {"message": 'Not found'}, 404
