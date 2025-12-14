from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube
from pytubefix.cli import on_progress

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Server is Running with PyTubeFix!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # PyTubeFix ka use karke data nikalenge
        yt = YouTube(url, on_progress_callback=on_progress)
        
        title = yt.title
        thumbnail = yt.thumbnail_url

        # Sabse safe quality (720p/360p with Audio) nikalna
        # Ye bina FFmpeg ke bhi chalti hai
        video_stream = yt.streams.get_highest_resolution()
        
        # Audio Only Stream
        audio_stream = yt.streams.get_audio_only()

        return jsonify({
            'status': 'success',
            'title': title,
            'thumbnail': thumbnail,
            'formats': [
                {
                    'quality': f"{video_stream.resolution} (Best Safe)",
                    'url': video_stream.url
                }
            ],
            'audio_url': audio_stream.url
        })

    except Exception as e:
        print(f"Error: {e}")
        # Agar error aaye to user ko dikhayein
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
