from flask import Flask, render_template, request, jsonify import requests import time import os

app = Flask(name) UPLOAD_FOLDER = 'uploads' os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/') def index(): return render_template('index.html')

@app.route('/start_commenting', methods=['POST']) def start_commenting(): post_url = request.form.get('post_url') delay = int(request.form.get('time', 30))

cookies_file = request.files.get('cookies')
comments_file = request.files.get('comments')

if not post_url or not cookies_file or not comments_file:
    return jsonify({'status': 'error', 'message': 'Missing required inputs'})

cookies_path = os.path.join(UPLOAD_FOLDER, 'cookies.txt')
comments_path = os.path.join(UPLOAD_FOLDER, 'comments.txt')
cookies_file.save(cookies_path)
comments_file.save(comments_path)

with open(cookies_path, 'r') as f:
    cookies_list = [line.strip() for line in f if line.strip()]

with open(comments_path, 'r') as f:
    comments_list = [line.strip() for line in f if line.strip()]

headers = {
    "User-Agent": "Mozilla/5.0"
}

success = 0
for idx, cookie in enumerate(cookies_list):
    for comment in comments_list:
        try:
            response = requests.post(
                post_url,
                data={"comment_text": comment},
                headers={"Cookie": cookie, **headers}
            )
            if response.status_code == 200:
                success += 1
                print(f"Commented with cookie {idx+1}")
            else:
                print(f"Failed with cookie {idx+1}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")

return jsonify({'status': 'success', 'message': f'Total {success} comments sent!'})

if name == 'main': app.run(host='0.0.0.0', port=10000)

