import os
from flask import Flask, render_template, request, jsonify
from ai_engine import generate_frontend_code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_update', methods=['POST'])
def chat_update():
    try:
        data = request.json
        response_data = generate_frontend_code(data.get('prompt'), data.get('current_html'))
        return jsonify(response_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Server Error", "html": ""}), 500

if __name__ == '__main__':
    print("🚀 Hybrid Builder Running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)