# ... existing code ...
from dotenv import load_dotenv
import os
import openai

# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

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