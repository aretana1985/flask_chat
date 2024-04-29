from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, render_template_string
from openai import OpenAI
import os
import traceback

app = Flask(__name__)

# Instantiate the OpenAI client with your API key
client = OpenAI(api_key=os.getenv('APIKEY'))

@app.route('/', methods=['GET', 'POST'])
def chat_view():
    ai_message = ""  # Initialize ai_message to an empty string
    if request.method == 'POST':
        user_message = request.form['user_input']
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}],
            )
            # Assuming 'response' has an attribute 'choices' which is a list,
            # and each choice has an attribute 'message', which is what you want to access:
            if response.choices:
                ai_message = response.choices[0].message.content  # Adjusted access method
            else:
                ai_message = "No response from AI."
        except Exception as e:
            ai_message = "Sorry, I could not fetch a response due to an error."
            print(traceback.format_exc())  # Print the full traceback for debugging

    # Render the template with the AI response
    return render_template_string(TEMPLATE, chat_response=ai_message)

# HTML template for the chat interface
TEMPLATE = """
<!doctype html>
<html>
<head><title>Chat powered by Moby</title></head>
<body>
    <h2>Grammar Improve Chat</h2>
    <form method="post">
        <input type="text" name="user_input" autofocus>
        <input type="submit" value="Send">
    </form>
    {% if chat_response %}
    <p><b>Response:</b> {{ chat_response }}</p>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=False)
