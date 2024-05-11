import requests, simpleaudio, tempfile, json

#1 リクエストの準備：
# サーバーのホストとポートを指定します。
# テキストと音声の種類（スピーカーID）をパラメータとして設定します。

host = "127.0.0.1" # "localhost"でも可能だが、処理が遅くなる
port = 50021

params = (
    ("text", "田中さんこんにちは、今日も良い天気ですね。"),
    ("speaker", 2) # 音声の種類をInt型で指定
)
# 以下の検索結果でどの数値がどういった声なのか記載されている
# https://github.com/VOICEVOX/voicevox_resource/search?q=styleId


#2. 音声データの生成：
# 最初のリクエストで音声データの生成条件をAPIサーバーに送信し、必要なメタデータ（音声のピッチ、速度など）を取得します。
# 取得したメタデータを使って、実際の音声データを生成します。

response1 = requests.post(
    f"http://{host}:{port}/audio_query",
    params=params
)

response2 = requests.post(
    f"http://{host}:{port}/synthesis",
    headers={"Content-Type": "application/json"},
    params=params,
    data=json.dumps(response1.json())
)

# 3.音声ファイルの保存と再生：
# 一時フォルダを作成し、そこに音声データをファイルとして保存します。
# 保存した音声ファイルをsimpleaudioライブラリを使用して再生します。

# 現在のディレクトリにファイルを保存
audio_file_path = "audi.wav"
with open(audio_file_path, "wb") as f:
    f.write(response2.content)

wav_obj = simpleaudio.WaveObject.from_wave_file(audio_file_path)
play_obj = wav_obj.play()
play_obj.wait_done()