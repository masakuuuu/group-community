from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView

app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html',
#                            title="Form sample",
#                            message="お名前は？")


# @app.route('/', methods=['POST'])
# def form():
#     field = request.form['field']
#     return render_template('index.html',
#                            title="Form sample",
#                            message="こんにちは、%sさん！" % field)


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
