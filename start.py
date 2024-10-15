from app import create_app, db

app = create_app()
print(app.instance_path)
with app.app_context():
  db.create_all()
