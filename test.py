import requests

res = requests.post("https://card-game-server-zfja.onrender.com/host")
print(res.json())