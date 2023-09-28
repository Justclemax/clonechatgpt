import openai

import  os
from flask import Flask, render_template
app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
@app.route("/")
def home():
    return render_template('index.html')

def build_convesation(messages : list) -> list[dict]:

    return [
        {"role":"user" if i % 2 == 0 else "assistant" , "content ": message}
        for i, message in enumerate(messages)
    ]
def event_stream (conversation :list[dict]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        stream = True
    )
    for line in response:
        text = line.choices[0].delta.get('content', '')
        if len(text):
            yield text

if __name__ == "__main__":
    conversation = build_convesation(messages=["Bonjour comment ça va", "Ça va bien et toi "])
    print(event_stream(conversation))
    for i in event_stream(conversation):
        print(i)