import requests

def generate_prompt(text_prompt):

    url = 'http://moody-zoos-return-35-232-142-40.loca.lt/api/v1/generate'
    request_body = {"prompt" : text_prompt}

    text_output = requests.post(url, json = request_body)

    return text_output.json()['results'][0]['text'] #returns a string

def process_prompt(text_prompt):

    four_chars = text_prompt[:4]

    starts_with_you = False

    if not text_prompt[-1] == ".":
        text_prompt = text_prompt + "."

    if not four_chars.lower() == "you ":

        if not text_prompt[0].islower():
            text_prompt = text_prompt[0].lower() + text_prompt[1:]

        text_prompt = "You " + text_prompt

    return text_prompt
    
userInput=input()
print(process_prompt(userInput))