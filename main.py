from bottle import Bottle, run, static_file, template, TEMPLATE_PATH
import os
from teams import team_app
from players import player_app
from database import get_db

TEMPLATE_PATH.append('./templates')

app = Bottle()
app.mount("/team", team_app)
app.mount("/player", player_app)

@app.route('/')
def home():
    return template('home') 

@app.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    print(f"Template paths: {TEMPLATE_PATH}") 
    run(app, host='localhost', port=8080, debug=True, reloader=True)