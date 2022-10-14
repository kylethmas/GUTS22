import requests


url = 'http://quick-kings-lose-34-134-245-36.loca.lt/api/v1/generate'
myobj = {"prompt" : 'You ask "what you need that baby for"'}

response = requests.post(url, json = myobj)

print(response.json())