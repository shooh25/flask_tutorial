import csv
from app import db,create_app
from app.models import Books

app = create_app()

# booksデータ初回登録
def insert_books():
  with open('./assets/BookList.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for line in reader:
      book = Books(
        id = line[0],
        author = line[1],
        title = line[2],
        publisher = line[3],
        price = line[4],
        isbn = line[5],
      )
      db.session.add(book)
    db.session.commit()

if __name__ == '__main__':
  with app.app_context():
    insert_books()