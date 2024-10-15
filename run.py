from app import create_app

app = create_app()

@app.route("/")
def index():
  return "Hello, World"

# このファイルを実行した際にローカルサーバーを立ち上げ
if __name__=="__main__":
  app.run(debug=True)

