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
        session['prompt_start'] = session['location'] + "," + session['art_style'] + "," + "D&D Greg Rutkowski high-detail quality-shading"
        session['text_display'] =  []
        session['text_display'].append("Your " + session['art_style'] + " adventure begins in (a) " + session['location'] + "!")
        return redirect(url_for('game'))
    return render_template('art_style.html')
    
@app.route("/game", methods=['GET', 'POST'])   
def game():
    user_input = "";
    return_type = play_game(user_input,0)
    if request.method == 'POST':
        #]print("are we here too?")
        user_input = request.form['user_input']
        while user_input.lower() != "quit": #user input never is quit :)
            print(user_input)
            return play_game(user_input,0)
            #return render_template('game.html', user_image = output_url)
    return return_type

#@app.route("/error", methods=['GET', 'POST'])   
#def error(img_link, error_text):
 #   return render_template('error.html', user_image = img_link, page_text)

    
def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

def play_game(user_input, count):
    output_url = ""
    #model = replicate.models.get("stability-ai/stable-diffusion")
    #output_url = model.predict(prompt = session['prompt_start'])[0]
    try:
        model = replicate.models.get("stability-ai/stable-diffusion")
        output_url = model.predict(prompt = session['prompt_start'])[0] #prompt="electric sheep, neon, synthwave")[0]
        print(output_url)
        
        if user_input != "":
            user_input = user_input + "."
            session['text_display'].append(user_input)
            try:
                kobold_ai_returned = generate_response(user_input, "http://tidy-clocks-exist-34-135-174-207.loca.lt/api/v1/")
            except:
                output_url = "https://images.clipartlogo.com/files/istock/previews/9266/92666913-error-message-on-tablet.jpg"
                #error(user_image = output_url, page_text = ["ERROR - Your kobold url has expired"])
                return render_template('game.html', user_image = output_url, page_text = ["ERROR - Your kobold url has expired"])
            print(kobold_ai_returned)
            session['prompt_start'] = user_input + kobold_ai_returned + "." + "D&D Greg Rutkowski high-detail quality-shading" + session['prompt_start']
            session['prompt_start'] = kobold_ai_returned + "." + session['prompt_start']
            kobold_ai_returned + "." + session['prompt_start']
            session['text_display'].append(kobold_ai_returned)
        
        print(session['prompt_start'])
        
    except:
       print("THIS INSIDE ERROR LOOP")
       if count >= 10:
            print("ERROR - Your replicate token expired")
            output_url = "https://images.clipartlogo.com/files/istock/previews/9266/92666913-error-message-on-tablet.jpg"
            session['text_display'].append("ERROR - Your replicate token has expired")
            #error(user_image = output_url, page_text = ["ERROR - Your replicate token expired"])
            return render_template('game.html', user_image = output_url, page_text = ["ERROR - Your replicate token expired"])
       count = count + 1
       play_game(user_input,count)
    
    print("!!!")
    print(output_url)
    #page_text = session['text_display'] #listToString(session['text_display'])
    return render_template('game.html', user_image = output_url, page_text = session['text_display'])
    #print("in the game")
    #print(session['location'])
    
    #return render_template('game.html')
