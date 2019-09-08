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
