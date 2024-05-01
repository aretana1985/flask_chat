from dotenv import load_dotenv
from flask import Flask, request, render_template_string, render_template, redirect, url_for
from openai import OpenAI
import os
import traceback
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Instantiate the OpenAI client with your API key
client = OpenAI(api_key=os.getenv('APIKEY'))

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Route for Email Improve functionality
@app.route('/chat', methods=['GET', 'POST'])
def chat_view():
    ai_message = "Hi , please  add your email so I can look into it"  # Initialize ai_message to an empty string
    if request.method == 'POST':
        user_message = request.form['user_input']
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}],
            )
            if response.choices:
                ai_message = response.choices[0].message.content
            else:
                ai_message = "No response from AI."
        except Exception as e:
            ai_message = "Sorry, I could not fetch a response due to an error."
            print(traceback.format_exc())  # Print the full traceback for debugging

    return render_template('chat.html', chat_response=ai_message)

# Route for Parts Search functionality
@app.route('/parts', methods=['GET', 'POST'])
def parts_search():
    ai_message= "Please add  competition part number or specs and ask for your Lenovo Comparable"
    if request.method == 'POST':
        user_message = request.form['user_input']
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}],
            )
            if response.choices:
                ai_message = response.choices[0].message.content
            else:
                ai_message = "No response from AI."
        except Exception as e:
            ai_message = "Sorry, I could not fetch a response due to an error."
            print(traceback.format_exc())  # Print the full traceback for debugging

    return render_template('parts_search.html')

# Add your TEMPLATE variable here
TEMPLATE = """
<!doctype html>
<html>
<head><title>Gizmodes</title></head>
<body>
    <h2>Please select one of our CHat Rooms</h2>

    <ul>
        <li><a href="/email">Email Improve</a></li>
        <li><a href="/parts">Parts Comparison</a></li>
        <li><a href="/find-rep">Find a Rep</a></li>
    </ul>
</body>
</html>

"""

if __name__ == '__main__':
    app.run(debug=False)
