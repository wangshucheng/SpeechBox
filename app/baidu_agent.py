import requests

asr_url = 'http://192.168.31.176:8001/upload'


def asr(file_path):
    print("start baidu asr")
    with open(file_path, 'rb') as file:
        response = requests.post(asr_url, files={'file': file})
        text = response.text
        print("end baidu asr.text:"+text)
        return text


tts_url = "http://192.168.31.176:8001/audio"


def tts(prompt, file_path):
    print("start baidu tts")
    response = requests.post(tts_url, data={'prompt': prompt})

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
            print("Audio file saved successfully!")
    else:
        print("Failed to retrieve audio file.")
