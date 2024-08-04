from flask import Flask    #flaskモジュールの中のFlaskをインポート
from flask import render_template   #render_templateをインポートすることでhtmlファイルを返すことができる

app=Flask(__name__)    #必須表現
@app.route("/")
def index():
    return render_template("login.html")



if __name__ == '__main__':  #実行用の表現
    app.run(debug=True)