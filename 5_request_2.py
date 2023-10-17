import requests

url = 'https://api.openweathermap.org/data/2.5/weather?lat=-25.7523712&lon=29.715950&appid=95b9aaca4c4d70262e60f63f8f3393ff'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, data = myobj)

print(x.text)
