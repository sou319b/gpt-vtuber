import openai

# OpenAI APIキーを設定
# openai.api_key = ''
import os
api_key = os.environ.get("OPENAI_API_KEY")

from dotenv import load_dotenv
load_dotenv()

def chat_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

if __name__ == "__main__":
    while True:
        user_input = input("あなた: ")
        if user_input.lower() in ["終了", "exit", "quit"]:
            break
        response = chat_with_openai(user_input)
        print("AI: " + response)