from flask import Flask, jsonify

app = Flask(__name__)

# Esempio di dati
data = [
    {"id": 1, "name": "Prodotto 1"},
    {"id": 2, "name": "Prodotto 2"},
    {"id": 3, "name": "Prodotto 3"}
]

@app.route('/')
def hello():
    return "Benvenuto all'API di test!"

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)