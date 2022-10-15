from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from uuid import uuid4
from flask import session
from flask_session import Session
from flask import request
import replicate
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)
@socketio.on('connect')
def connect():
    session['sid'] = request.sid
    

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('game.html')
    return render_template('index.html')
    
@app.route("/", methods=['GET', 'POST'])   
def game():
    model = replicate.models.get("stability-ai/stable-diffusion")
    output_url = model.predict(prompt="electric sheep, neon, synthwave")[0]
    print(output_url)
    webbrowser.open(output_url)