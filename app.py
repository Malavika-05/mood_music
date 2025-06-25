from flask import Flask, render_template, request
from textblob import TextBlob
import json
import re
import socket

app = Flask(__name__)

with open('static/songs/lyrics.json') as f:
    SONGS = json.load(f)

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    filtered_songs = {k: v for k, v in SONGS.items() if query in k.lower()}
    return render_template('index.html', songs=filtered_songs, query=query)

@app.route('/detect', methods=['POST'])
def detect():
    title = request.form['title']
    lyrics = request.form['lyrics']

    blob = TextBlob(lyrics)
    polarity = blob.sentiment.polarity
    mood = classify_mood(polarity)

    print(f"Detected mood: {mood}")  # debug

    try:
        send_metric(f"mood_music.{mood}", 1)
        send_metric("mood_music.total", 1)
        print(f"Metric sent: mood_music.{mood}")  # debug
    except Exception as e:
        print(f"Metric send failed: {e}")  # debug

    # Convert to lowercase and underscores: e.g., "Someone Like You" → "someone_like_you"
    raw_name = title.split(' - ')[0].strip()
    song_name = re.sub(r'\W+', '_', raw_name).lower()

    return render_template('result.html', title=title, mood=mood, song_name=song_name)



from textblob import TextBlob

def classify_mood(p):
    if p > 0.6:
        return 'upbeat'
    elif p > 0.3:
        return 'happy'
    elif p > 0:
        return 'romantic'
    elif p == 0:
        return 'carefree'
    elif p < -0.5:
        return 'angry'
    else:
        return 'sad'
    
def send_metric(metric, value):
    message = f"{metric}:{value}|c"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), ("172.18.0.3", 8125))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



