import requests
import json
from pydub import AudioSegment
from pydub.playback import play

def test_voicevox(text):
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
    test_text = "こんにちは、これはテストです。しゃべった内容はこの文章です。"
    test_voicevox(test_text)