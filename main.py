# ... existing code ...
from dotenv import load_dotenv
import os
import openai
import subprocess
from pydub import AudioSegment
from pydub.playback import play
import requests
import json

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

def speak_with_voicevox(text):
    # 音声クエリを生成
    query_response = requests.post(
        "http://localhost:50021/audio_query",
        params={"text": text, "speaker": 1}
    )
    query_response.raise_for_status()
    audio_query = query_response.json()

    # 音声合成
    synthesis_response = requests.post(
        "http://localhost:50021/synthesis",
        headers={"Content-Type": "application/json"},
        params={"speaker": 1},
        data=json.dumps(audio_query)
    )
    synthesis_response.raise_for_status()

    # 音声を再生
    with open("output.wav", "wb") as f:
        f.write(synthesis_response.content)
    
    # pydubで音声を再生
    sound = AudioSegment.from_wav("output.wav")
    play(sound)

if __name__ == "__main__":
    while True:
        user_input = input("あなた: ")
        if user_input.lower() in ["終了", "exit", "quit"]:
            break
        response = chat_with_openai(user_input)
        print("AI: " + response)
        speak_with_voicevox(response)