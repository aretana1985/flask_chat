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
@app.route('/chat')
def home():
    return render_template('home.html')

# Route for Email Improve functionality
@app.route('/email', methods=['GET', 'POST'])
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
        part_number = request.form['part_number']
        
        # Fetch data from StockInTheChannel
        response = requests.get(f'https://us.stockinthechannel.com/Search?Query={part_number}')
        if response.status_code == 200:
            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract part information (this logic may vary depending on the actual page structure)
            part_details = [item.text.strip() for item in soup.select('.some-css-selector')] # Replace '.some-css-selector' with actual selector for part info
        else:
            part_details = ["Unable to fetch part information."]
        
        return render_template('parts_result.html', part_number=part_number, part_details=part_details)

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
