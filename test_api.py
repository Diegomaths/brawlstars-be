from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def get_user():
    url = 'https://brawlstars-be.ew.r.appspot.com/api/v1/get_user'
    payload = 'user2'
    print(0)
    try:
        print(1)
        response = requests.post(url, json=payload)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print(e)
        return str(e)

if __name__ == '__main__':
    app.run("localhost",port=5000)
