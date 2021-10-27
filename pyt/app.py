from flask import Flask
from flask import request, send_file
import json
import os


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def calculate():
    return "succ"

# @app.route('/')
# def index():
#     return send_file("index.html")



# @app.route('/file')
# def filesend():
#     cwd = os.getcwd()
#     return render_template("index.html")
#     #return send_from_directory(cwd, "index.html")
#     #return send_from_directory()

# @app.route('/json')
# def myjson():
#     return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

# #http://localhost:5000/sum?func=(x%y)/y&x=11
# @app.route('/sum')
# def sum():
#     func = request.args.get('func')
#     fr = request.args.get('fr')
#     to = request.args.get('to')
#     x = request.args.get('x')
    
#     return str(Sum(x, func, fr, to).result())

if __name__ == '__main__':
    app.run(debug=True)
    app.run(ssl_context='adhoc')
    