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
from app.main import main
from app.kobold_ai import generate_response, process_prompt

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
        return redirect(url_for('art'))
    return render_template('location.html')
    
@app.route("/art_style", methods=['GET', 'POST'])   
def art():
    if request.method == 'POST':
        print(request.form['art_style'])
        session['art_style'] = request.form['art_style']
        session['prompt_start'] = session['location'] + "," + session['art_style']
        return redirect(url_for('game'))
    return render_template('art_style.html')
    
@app.route("/game", methods=['GET', 'POST'])   
def game():
    user_input = "";
    return_type = play_game(user_input)
    if request.method == 'POST':
        user_input = request.form['user_input']
        while user_input.lower() != "quit": #user input never is quit :)
            #edit this to do full stops
            return play_game(user_input)
            #return render_template('game.html', user_image = output_url)
    return return_type
    
def play_game(user_input):
    
    model = replicate.models.get("stability-ai/stable-diffusion")
    if user_input != "":
        session['prompt_start'] = user_input + "." + session['prompt_start']
        
    print(session['prompt_start'])
    #print(generate_response(user_input + ".", "http://bitter-beds-begin-35-238-79-164.loca.lt/api/v1/"))
    
    output_url = model.predict(prompt = session['prompt_start'])[0] #prompt="electric sheep, neon, synthwave")[0]
    print(output_url)
    return render_template('game.html', user_image = output_url, page_text = ' TEST text')
    #print("in the game")
    #print(session['location'])
    
    #return render_template('game.html')
