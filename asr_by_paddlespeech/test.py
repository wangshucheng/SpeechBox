import requests

# url = "http://localhost:8001/audio"
# url = "http://172.21.73.101:8001/audio"
url = "http://192.168.31.176:8001/audio"

data = {'prompt': '今天天气十分不错。'}

response = requests.post(url, data=data)

if response.status_code == 200:
    with open("audio.wav", "wb") as f:
        f.write(response.content)
        print("Audio file saved successfully!")
else:
    print("Failed to retrieve audio file.")
