from flask import Blueprint, request, render_template
from .models import Books
import requests
from sqlalchemy import or_
from app import db

bp = Blueprint("bp", __name__)

# Google Books API
def get_book_from_gb(isbn):
  url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key=AIzaSyDs9EOsXqjR6NxuIvPm1cC8w_A6GhK3yIg"
  response = requests.get(url)
  print(response.json())
  if response.status_code == 200:
    data = response.json()
    total_items = data.get('totalItems')
    if total_items:
      volume_info = data["items"][0]["volumeInfo"]
      title = volume_info.get("title")
      authors = ", ".join(volume_info.get("authors"))
      return [title, authors, isbn]
    else:
      return None
  else:
    return None
  
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

# タイトル,著者検索
@bp.route("/", methods=['GET'])
def search_book():
  q = request.args.get('q', '') # 検索クエリ
  
  # 検索クエリが空の場合はHTMLのロードのみ
  if q == '':
    return render_template(
      "index.html"
    )
  
  cursor = request.args.get('cursor', type=int) # カーソル
  limit = 5 # 取得上限数
  
  prev_cursor = None #前ページへのカーソル
  query = Books.query
  
  if cursor:
    # カーソルより後ろの書籍情報を取得
    next_query = query.filter(Books.id >= cursor)
    next_query = next_query.filter(or_(Books.title.like(f'%{q}%'), Books.author.like(f'%{q}%')))
    
    # カーソル直前の5件を取得
    prev_query = query.filter(Books.id < cursor)
    prev_query = prev_query.filter(or_(Books.title.like(f'%{q}%'), Books.author.like(f'%{q}%')))
    prev_books = prev_query.order_by(Books.id.desc()).limit(limit).all()
    
    # 5件の最後の要素のIDを前ページへのカーソルに指定
    if prev_books:
      prev_cursor = prev_books[-1].id
    
  else:
    # 初期リクエスト,カーソル指定なしの場合
    next_query = query.filter(or_(Books.title.like(f'%{q}%'), Books.author.like(f'%{q}%')))
  
  # 書籍情報を5+1件まで取得
  books = next_query.order_by(Books.id).limit(limit + 1).all()
  
  # 次ページへのカーソルと書籍情報5件を作成
  next_cursor = None
  if len(books) > limit:
    next_cursor = books[-1].id
    books = books[:-1]
  
  # デバッグ用
  print(books, next_cursor, prev_cursor)
  
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
  
  return render_template(
    'index.html',
    q=q,
    books=responce,
    next_cursor=next_cursor,
    prev_cursor=prev_cursor,
  )

# 書籍登録
@bp.route("/books", methods=['POST'])
def add_book():
  data = request.get_json()
  isbn = data.get('isbn')
  
  if Books.query.filter_by(isbn=isbn).first():
    return {"message": "A book with the same ISBN is already exist."}, 400
  
  book = get_book_from_gb(isbn)
  if not book:
    return {"message": "A book with the ISBN is not found."}, 404
  
  # 最新のIDを取得
  new_book = Books(
    author = book[0],
    title = book[1],
    isbn = book[2],
  )
  
  db.session.add(new_book)
  db.session.commit()
  
  return book
  