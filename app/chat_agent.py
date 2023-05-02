import requests
import json
url = "http://192.168.31.176:8000"




def ask(prompt,history):
    try:
        data = {"prompt": prompt, "history": history}
        res = requests.post(url=url, json=data)
        res_json = res.json()
        print(res_json)
        if res_json["status"] == 200:
            response = res_json["response"]
            history = res_json["history"]
            return response, history, res.text
        else:
            return None, history, res.text
    except Exception as e:
        print("发生异常：", e)
        raise e
        return None, history, res.text