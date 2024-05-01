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
    ai_message = ""  # Initialize ai_message to an empty string
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
<head><title>Home</title></head>
<body>
    <h2>Welcome to Moby Chat</h2>

    <ul>
        <li><a href="/email">Email Improve</a></li>
        <li><a href="/parts">Parts Search</a></li>
        <li><a href="/find-rep">Find a Rep</a></li>
    </ul>
</body>
</html>

"""

if __name__ == '__main__':
    app.run(debug=False)
