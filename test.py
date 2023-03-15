import requests

url = "https://maps.googleapis.com/maps/api/timezone/json?location=39.6034810%2C-119.6822510&timestamp=1331161200&key=AIzaSyC-s1n8l1_bePWAAFjiCFVaQ6EFA2a_o7E"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)