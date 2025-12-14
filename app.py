from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Server is Running! Shivam's Backend is Live."

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Data extract karna
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            # Video Links (With Audio)
            formats = []
            for f in info['formats']:
                if f.get('ext') == 'mp4' and f.get('acodec') != 'none':
                    formats.append({
                        'quality': f.get('format_note', 'Standard'),
                        'url': f['url']
                    })
            
            # Best formats ko filter karke last 2-3 hi dikhayenge taaki user confuse na ho
            clean_formats = formats[-3:] 

            return jsonify({
                'status': 'success',
                'title': title,
                'thumbnail': thumbnail,
                'formats': clean_formats,
                # Audio Only Link (MP3 approach)
                'audio_url': info['formats'][0]['url'] # Fallback audio
            })

    except Exception as e:
        return jsonify({'error': 'Invalid URL or YouTube Blocked Request'}), 500

if __name__ == '__main__':
    app.run(debug=True)