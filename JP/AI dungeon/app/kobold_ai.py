import requests

#api_link=http://bitter-beds-begin-35-238-79-164.loca.lt/api/v1/

def generate_response(text_prompt, api_link):

    text_prompt = process_prompt(text_prompt)

    url = api_link + "generate"
    request_body = {"prompt" : text_prompt}

    text_response = requests.post(url, json = request_body).json()['results'][0]['text'] #returns a string

    found = False
    i = 0
    while found == False and i < len(text_response):
        if text_response[-i-1] == ',' or text_response[-i-1] == '.':
            
            end_of_sentence = len(text_response) - i
            text_response = text_response[:end_of_sentence]

            if text_response[-1] == ',':
                text_response = text_response[:-1] + "."
            found = True
        i+=1

    return text_response

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
