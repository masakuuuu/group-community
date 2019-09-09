# 準備編

## 1. Python のインストール

以下のサイトより Python をインストール

https://www.python.org/downloads/

※PATH を通すことを忘れずに

- Path の通し方まとめ

https://www.javadrive.jp/python/install/index3.html

- インストール確認コマンド

  PowerShell などで `python --version`

## 2. VSCode のインストール

- Python 開発に便利なエディタ

https://code.visualstudio.com/

- 関連記事

  VS Code で Python するために必要なこと

  https://www.atmarkit.co.jp/ait/articles/1805/22/news043.html

# 基本編

## 1. 静的ファイルを返すだけの http.server の利用

学習用のモジュールのため、プロダクトとしては不向き（同時アクセスに弱い？）

### フォルダの作成

デスクトップに「python_folder」というフォルダを作成

### index.html の作成

簡単な HTML ページを作成

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>Index</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <h1>Index</h1>
    <p>This is sample page!!</p>
  </body>
</html>
```

### app.py の作成

HTTPServer を起動するためのプログラムを作成

app.py に以下のようなプロラムを作成

```python
from http.server import SimpleHTTPRequestHandler, HTTPServer

server = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```

- HTTPServer の起動

app.py をコマンドプロンプト（PowerShell 等）で実行

実行コマンド

（VSCode 場のターミナルからも実行可能）

```shell
python app.py
```

- ブラウザで以下にアクセス

http://localhost:8000/

## 2. クライアントのリクエストを受ける http.server の利用

BaseHTTPRequestHandler の利用

- app.py の修正

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Sample web-server!!!')
        return

server = HTTPServer(('', 8000), HelloServerHandler)
server.serve_forever()
```

## 3. Python で指定した HTML を返す

- app.py を修正

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

with open('index.html', mode='r') as f:
    index = f.read()


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(index.encode('utf-8'))
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()
```

## 4. Python で処理した値を HTML に流し込む

HTML 側にプレースホルダを設定して、Python 側で処理した値を流し込む

- index.html を修正

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>{title}</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <h1>{title}</h1>
    <p>{message}</p>
  </body>
</html>
```

Python 側を修正して値を流し込めるようにする

- app.py を修正

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

with open('index.html', mode='r') as f:
    index = f.read()


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='ようこそ、HTTPServerの世界へ！'
        )
        self.wfile.write(html.encode('utf-8'))
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()
```

## ルーティング

- index.hmtl の編集

※ `{` や `}` は Python のフォーマット済みテキストを利用する倍は、フィールドとして予約されているため、改行などされると正しくフォーマットできずに落ちる

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>{title}</title>
    <meta charset="utf-8" />
    <style>
      body {
         {
          margin: 10px;
        }
      }
      h1 {
         {
          color: lightgray;
          font-size: 36pt;
        }
      }
      p {
         {
          font-size: 16pt;
        }
      }
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <p>{message}</p>
  </body>
</html>
```

- next.html を作成

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>{title}</title>
    <meta charset="utf-8" />
    <style>
      body {{margin: 10px;}}
      h1 {{text-align:right;}}
      p {{font-size: 16pt;}}
      pre {{background-color:aliceblue:}}
    </style>
  </head>
  <body>
    <h1>Next Page</h1>
    <p>{message}</p>
    <pre>{data}</pre>
  </body>
</html>
```

- app.py の修正

ルーティングを実装

```Python
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        _url = urlparse(self.path)
        if(_url.path == '/'):
            self.index()
        elif(_url.path == '/next'):
            self.next()
        else:
            self.error()

    # index action.
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='ようこそ、HTTPServerの世界へ！'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # next action.
    def next(self):
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message='This is Next Page.',
            data='{\n data:"this is data."\n}'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # error action
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()
```

'/' にアクセスすると 'index.hmtl' が表示される

'/next' にアクセスすると 'next.html' が表示される

上記以外だと 404 のエラーページが表示される

## ルーティングの修正

保守性と可読性を上げるためにルーティングを修正

```Python
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()


routes = []


def route(path, method):
    routes.append((path, method))


# add route settiong.
route('/', 'index')
route('/index', 'index')
route('/next', 'next')


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if(r[0] == _url.path):
                eval('self.' + r[1] + '()')
                return
        self.error()
        return

    # index action.
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='ようこそ、HTTPServerの世界へ！'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # next action.
    def next(self):
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message='This is Next Page.',
            data='{\n data:"this is data."\n}'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # error action
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()
```

## URL パラメータを挿入する

- app.py を修正

変更ポイント

インポートするパッケージに `parse_qs` を追加

next メソッドに処理を追加

```python
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()


routes = []


def route(path, method):
    routes.append((path, method))


# add route settiong.
route('/', 'index')
route('/index', 'index')
route('/next', 'next')


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if(r[0] == _url.path):
                eval('self.' + r[1] + '()')
                return
        self.error()
        return

    # index action.
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='ようこそ、HTTPServerの世界へ！'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # next action.
    def next(self):
        _url = urlparse(self.path)
        query = parse_qs(_url.query)
        id = query['id'][0]
        password = query['pass'][0]
        msg = 'id=' + id + ', password=' + password
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message=msg,
            data=query
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # error action
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()

```

## フォーム送信を行う

- index.html の修正

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>{title}</title>
    <meta charset="utf-8" />
    <style>
      body {
         {
          margin: 10px;
        }
      }
      h1 {
         {
          color: lightgray;
          font-size: 36pt;
        }
      }
      p {
         {
          font-size: 16pt;
        }
      }
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <p>{message}</p>
    <div>
      <form method="post" action="/">
        <input type="text" name="textfield" />
        <input type="submit" />
      </form>
    </div>
  </body>
</html>
```

- app.py の修正

変更ポイント

FieldStorage というパッケージを追加

POST メソッドの追加

```python
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()


routes = []


def route(path, method):
    routes.append((path, method))


# add route settiong.
route('/', 'index')
route('/index', 'index')
route('/next', 'next')


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if(r[0] == _url.path):
                eval('self.' + r[1] + '()')
                return
        self.error()
        return

    def do_POST(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        res = form['textfield'].value
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message='you typed: ' + res,
            data=form
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # index action.
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='Form送信'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # next action.
    def next(self):
        _url = urlparse(self.path)
        query = parse_qs(_url.query)
        id = query['id'][0]
        password = query['pass'][0]
        msg = 'id=' + id + ', password=' + password
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message=msg,
            data=query
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # error action
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()

```

## 送信されない値のチェック

- index.html の修正

```html
<!DOCTYPE html>
<html lang="jp">
  <head>
    <title>{title}</title>
    <meta charset="utf-8" />
    <style>
      body {
         {
          margin: 10px;
        }
      }
      h1 {
         {
          color: lightgray;
          font-size: 36pt;
        }
      }
      p {
         {
          font-size: 16pt;
        }
      }
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <p>{message}</p>
    <div>
      <form method="post" action="/">
        <div>
          <input type="checkbox" id="ck1" name="ckeck1" />
          <label for="ck1">Checkbox 1</label>
        </div>
        <div>
          <input type="checkbox" id="ck2" name="ckeck2" />
          <label for="ck2">Checkbox 2</label>
        </div>
        <input type="submit" />
      </form>
    </div>
  </body>
</html>
```

- app.py の修正

変更ポイント

POST メソッドの中身だけを修正

```python
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()


routes = []


def route(path, method):
    routes.append((path, method))


# add route settiong.
route('/', 'index')
route('/index', 'index')
route('/next', 'next')


class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if(r[0] == _url.path):
                eval('self.' + r[1] + '()')
                return
        self.error()
        return

    def do_POST(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

        if 'check1' in form:
            ck1 = True
        else:
            ck1 = False
        if 'check2' in form:
            ck2 = True
        else:
            ck2 = False
        res = 'Chek1: ' + str(ck1) + \
            ', Check2: ' + str(ck2)
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message=res,
            data=form
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # index action.
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='Form送信'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # next action.
    def next(self):
        _url = urlparse(self.path)
        query = parse_qs(_url.query)
        id = query['id'][0]
        password = query['pass'][0]
        msg = 'id=' + id + ', password=' + password
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message=msg,
            data=query
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # error action
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return


HTTPServer(('', 8000), HelloServerHandler).serve_forever()
```
