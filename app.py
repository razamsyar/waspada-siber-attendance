from flask import Flask, render_template, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Initialize click counter
if not os.path.exists('clicks.json'):
    with open('clicks.json', 'w') as f:
        json.dump({'clicks': 0}, f)

def get_clicks():
    with open('clicks.json', 'r') as f:
        return json.load(f)['clicks']

def increment_clicks():
    data = {'clicks': get_clicks() + 1}
    with open('clicks.json', 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    increment_clicks()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin')
def admin():
    clicks = get_clicks()
    return render_template('admin.html', clicks=clicks)

if __name__ == '__main__':
    app.run(debug=True) 