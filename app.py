from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Shivam's Server is UP and Running!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # 🔴 YAHAN MAGIC FIX KIYA HAI 🔴
    # Hum YouTube ko bol rahe hain ki hum 'Android' client hain
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info extract karo
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            # Formats filter karo
            formats = []
            
            # Sirf wo formats lo jisme video + audio dono ho (url check)
            for f in info['formats']:
                if f.get('url'): 
                    # Logic: Mp4 extension aur Audio codec hona chahiye
                    if f.get('ext') == 'mp4' and f.get('acodec') != 'none':
                        formats.append({
                            'quality': f.get('format_note', 'HD'),
                            'url': f['url']
                        })
            
            # Agar direct combo nahi mila, toh best available URL bhej do
            if not formats:
                formats.append({
                    'quality': 'Standard',
                    'url': info['url'] # Fallback
                })

            # Sirf last 2 best quality bhejo
            clean_formats = formats[-2:] 

            return jsonify({
                'status': 'success',
                'title': title,
                'thumbnail': thumbnail,
                'formats': clean_formats,
                'audio_url': info['formats'][0]['url'] # Fallback audio
            })

    except Exception as e:
        # Error print karega logs mein taaki hum pakad sakein
        print(f"ERROR: {str(e)}")
        return jsonify({'error': 'YouTube Blocked this Server IP. Try again in 5 mins.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
