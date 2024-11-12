from app import create_app

app = create_app()

# このファイルを実行した際にローカルサーバーを立ち上げ
if __name__=="__main__":
  app.run(debug=True, port=8888)

