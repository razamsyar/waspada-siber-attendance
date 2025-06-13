from flask import Flask, render_template, redirect, url_for, jsonify
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize click counter
if not os.path.exists('clicks.json'):
    with open('clicks.json', 'w') as f:
        json.dump({'clicks': 0}, f)

def get_clicks():
    try:
        with open('clicks.json', 'r') as f:
            return json.load(f)['clicks']
    except Exception as e:
        logger.error(f"Error reading clicks: {str(e)}")
        return 0

def increment_clicks():
    try:
        data = {'clicks': get_clicks() + 1}
        with open('clicks.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Error incrementing clicks: {str(e)}")

@app.route('/')
def index():
    logger.info("Accessing index page")
    return render_template('index.html')

@app.route('/confirm', methods=['POST'])
def confirm():
    logger.info("Processing confirmation")
    increment_clicks()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    logger.info("Accessing success page")
    return render_template('success.html')

@app.route('/admin')
def admin():
    logger.info("Accessing admin page")
    clicks = get_clicks()
    return render_template('admin.html', clicks=clicks)

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"An error occurred: {str(error)}")
    return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run() 