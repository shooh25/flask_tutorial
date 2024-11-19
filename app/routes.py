from flask import Blueprint, request
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
  cursor = request.args.get('cursor', type=int)
  limit = 5
  
  prev_cursor = None
  query = Books.query
  if cursor:
    # 次の5件を取得
    next_query = query.filter(Books.id > cursor)
    next_query = next_query.filter(Books.title.like(f'%{title}%'))
    
    # 前の5件を取得してカーソルを指定
    prev_query = query.filter(Books.id < cursor)
    prev_query = prev_query.filter(Books.title.like(f'%{title}%'))
    prev_books = prev_query.order_by(Books.id.desc()).limit(limit).all()
    
    if prev_books:
      prev_cursor = prev_books[-1].id
    
  else:
    # 初期リクエスト,カーソル指定なしの場合
    next_query = query.filter(Books.title.like(f'%{title}%'))
  
  # 該当の書籍情報を５件まで取得
  books = next_query.order_by(Books.id).limit(limit + 1).all()
  
  next_cursor = None
  if len(books) > limit:
    next_cursor = books[-1].id
    books = books[:-1]
  
  if books:
    responce = [
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
    return {
      'books': responce,
      'next_cursor': next_cursor,
      'prev_cursor': prev_cursor,
    }
    
  return {"message": 'Not found'}, 404
