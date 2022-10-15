from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from uuid import uuid4
from flask import session
from flask_session import Session
from flask import request, url_for, redirect
import replicate
import webbrowser
from PIL import Image
import urllib.request

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
        return redirect(url_for('location'))
    return render_template('index.html')
    
@app.route("/location", methods=['GET', 'POST'])   
def location():
    if request.method == 'POST':
        print(request.form['location'])
        session['location'] = request.form['location']
        return redirect(url_for('art'))#, user_image = output_url)
    return render_template('location.html')
    
@app.route("/art_style", methods=['GET', 'POST'])   
def art():
    if request.method == 'POST':
        print(request.form['art_style'])
        session['art_style'] = request.form['art_style']
        return redirect(url_for('game'))#, user_image = output_url)
    return render_template('art_style.html')
    
@app.route("/game", methods=['GET', 'POST'])   
def game():
    #model = replicate.models.get("stability-ai/stable-diffusion")
    #this just takes us to the lil website - we dont like this
    #output_url = model.predict(prompt="electric sheep, neon, synthwave")[0]
    #print(output_url)
    #return render_template('game.html', user_image = output_url)
    print("in the game")
    print(session['location'])
    return render_template('game.html')
    #webbrowser.open(output_url)
    #print("edited this out so i dont use up all my API time")
    #return render_template('location.html')

