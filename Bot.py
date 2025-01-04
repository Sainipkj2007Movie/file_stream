import os
import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# Telegram Bot Token (Replace with your token)
BOT_TOKEN = "7319716758:AAFoejp2N8CEdzkXEF-EsvVAJd-D_k8x_uo"

# Helper Function: Get File URL from Telegram
def get_file_url(file_id):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    response = requests.get(api_url, params={"file_id": file_id})
    response.raise_for_status()
    file_path = response.json()["result"]["file_path"]
    return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

# Streaming Handler
@app.route('/stream/<file_id>', methods=['GET'])
def stream_file(file_id):
    try:
        # Get the file URL from Telegram
        file_url = get_file_url(file_id)
        
        # Get Range Header from the Client
        range_header = request.headers.get("Range", None)
        headers = {}

        # Handle Range Requests
        if range_header:
            range_match = range_header.replace("bytes=", "").split("-")
            start = int(range_match[0])
            end = range_match[1]
            end = int(end) if end else ""

            headers["Range"] = f"bytes={start}-{end}"

        # Stream the File in Chunks
        with requests.get(file_url, headers=headers, stream=True) as r:
            r.raise_for_status()
            content_type = r.headers.get("Content-Type", "application/octet-stream")
            content_range = r.headers.get("Content-Range")
            content_length = r.headers.get("Content-Length")

            # Send response in chunks
            return Response(
                r.iter_content(chunk_size=10 * 1024 * 1024),  # 10 MB chunks
                status=206 if range_header else 200,
                content_type=content_type,
                headers={
                    "Content-Range": content_range,
                    "Content-Length": content_length,
                    "Accept-Ranges": "bytes",
                },
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Telegram File Streaming Service",
        "usage": "/stream/<file_id>"
    })

# Run the Application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
