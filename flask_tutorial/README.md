# 準備編

Python のフレームワークとしては`Django`が主流ではあるが、小規模アプリには`Flask`がオススメ

軽量かつ必要機能が局所的なためビギナー向き

マイクロフレームワーク

## Flask のインストール

コマンドプロンプト等で以下のコマンドを実行

※`pip`コマンドは Python インストール時に Path を通している前提

```shell
pip install Flask
```

## Flask アプリの作成

新たに`flask_app`というフォルダを作成し、`app.py` という Python ファイルを作成

以下のとおり `app.py` を作成

```Python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask Workd!'

```

コマンドプロンプトで`app.py` が保存されている階層まで移動し、以下のコマンドを実行

```Python
set FLASK_APP=app.py
flask run
```

### Flask アプリを Python コマンドで実行する

- `app.py`を以下の通り修正

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask Workd!'


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
```

## Flask で HTML ファイルを利用する

※Flask の HTML テンプレートは `templates`というフォルダの中で管理する。

新規作成する `index.html` も `app.py` と同階層に作成する`templates`というフォルダの中に入れる

- `index.html` の作成

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>Index</title>
    <meta charset="utf-8" />
    <style>
      body {
        margin: 10px;
      }

      h1 {
        color: lightgray;
        font-size: 30pt;
      }

      p {
        font-size: 14pt;
      }
    </style>
  </head>

  <body>
    <h1>Index</h1>
    <p>This is Flask sample.</p>
  </body>
</html>
```

- `app.py` の修正

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
```

## テンプレートファイルに Python で処理した値を流し込む

- `index.html`を以下のとおり修正

修正ポイント

H1 と p タグにプレースホルダをセット

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>Index</title>
    <meta charset="utf-8" />
    <style>
      body {
        margin: 10px;
      }

      h1 {
        color: lightgray;
        font-size: 30pt;
      }

      p {
        font-size: 14pt;
      }
    </style>
  </head>

  <body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
  </body>
</html>
```

- `app.py` を以下の通り修正

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title="Index with Jinja",
                           message="これはJinjaテンプレートの利用例です。！")


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
```

## リクエストパラメータを処理する

- `app.py` を以下の通り修正

```py
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title="Index with Jinja",
                           message="これはJinjaテンプレートの利用例です。！")


@app.route('/<id>/<password>')
def index2(id, password):
    msg = 'id: %s, password: %s' % (id, password)
    return render_template('index.html',
                           title="Index with Jinja",
                           message=msg)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
```

## CSS を外部ファイルとして切り出す

Flask では静的ファイルは`static`というフォルダに追加する

`static` フォルダを作成

＊ `static` フォルダ内に `style.css` を新規作成し以下の通り修正する

```css
body {
  margin: 10px;
  background-color: aliceblue;
}

h1 {
  color: lightsteelblue;
  font-size: 36pt;
  margin: 0px;
}

p {
  font-size: 14pt;
}
```

- `index.html` を以下の通り修正する

CSS を適応させる

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>Index</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="{{url_for('static', filename='style.css')}}" />
  </head>

  <body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
  </body>
</html>
```

## Flask でのフォーム送信

- `index.html` を以下の通り修正

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>Index</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="{{url_for('static', filename='style.css')}}" />
  </head>

  <body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <div>
      <form method="post" ation="/">
        <input type="text" name="field" />
        <input type="submit" />
      </form>
    </div>
  </body>
</html>
```

- `app.py` を以下の通り修正

```py
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           title="Form sample",
                           message="お名前は？")


@app.route('/', methods=['POST'])
def form():
    field = request.form['field']
    return render_template('index.html',
                           title="Form sample",
                           message="こんにちは、%sさん！" % field)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
```

## Flask での API 作成

### メソッドベース・ディスパッチ

特定のリクエストに対して GET メソッドと POST メソッドで処理を分けることができる

GET の対になる POST 処理が分散しないため、管理しやすい

API 作成にはうってつけ？

- `app.py`を以下の通り修正

```python
from flask.views import MethodView

app = Flask(__name__)

class HelloAPI(MethodView):
    send = ''

    def get(self):
        return render_template('next.html',
                               title='Next page',
                               message='何か書いてください。',
                               send=HelloAPI.send)

    def post(self):
        HelloAPI.send = request.form.get('send')
        return render_template('next.html',
                               title='Next page',
                               message='You send: ' + HelloAPI.send,
                               send=HelloAPI.send)


app.add_url_rule('/hello/', view_func=HelloAPI.as_view('hello'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')

```

`app.add_url_rule`メソッドでルーティングと呼び出すクラスを設定

リクエスト時のメソッドによって呼び出す処理を分ける

- `next.html`を新規作成

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>Index</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="{{url_for('static', filename='style.css')}}" />
  </head>

  <body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <div>
      <form method="post" ation="/hello/">
        <input type="text" name="send" value="{{ send }}" />
        <input type="submit" />
      </form>
    </div>
  </body>
</html>
```

## セッションについて

セッション ID をキーにしてユーザ毎にデータを別々に保持する

- 'app.py' を以下の通り修正

変更ポイント

flask のモジュール読み込み箇所

HelloAPI の各メソッド

```py
from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView

app = Flask(__name__)

app.secret_key = b'abcdefghjik'


class HelloAPI(MethodView):
    send = ''

    def get(self):
        if 'send' in session:
            msg = 'send: ' + session['send']
            send = session['send']
        else:
            msg = '何か書いてください。'
            send = ''
        return render_template('next.html',
                               title='Next page',
                               message=msg,
                               send=send)

    def post(self):
        session['send'] = request.form['send']
        return redirect('/')


app.add_url_rule('/', view_func=HelloAPI.as_view('hello'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')

```
