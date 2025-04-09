from flask import Flask, request, Response
import requests
import time

app = Flask(__name__)

html_code = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Commenter</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .container {
            margin-top: 50px;
            background: #111;
            padding: 30px;
            border-radius: 15px;
            display: inline-block;
        }
        input, button, textarea {
            padding: 10px;
            margin: 10px;
            width: 250px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
        }
        button {
            background-color: #0f0;
            color: #000;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx</h1>
    <div class="container">
        <form action="/start_commenting" method="post">
            <textarea name="comments" placeholder="Enter comments (one per line)" rows="6" required></textarea><br>
            <input type="text" name="cookie" placeholder="Enter Facebook Cookie" required><br>
            <input type="text" name="post_url" placeholder="Facebook Post URL" required><br>
            <input type="number" name="delay" placeholder="Delay in seconds" required><br>
            <button type="submit">Submit Details</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return Response(html_code, mimetype='text/html')

@app.route('/start_commenting', methods=['POST'])
def comment():
    comments_raw = request.form['comments']
    post_url = request.form['post_url']
    delay = int(request.form['delay'])
    cookie = request.form['cookie']

    comments = comments_raw.strip().split('\n')

    headers = {
        "cookie": cookie,
        "user-agent": "Mozilla/5.0"
    }

    result_html = "<h2 style='color:lime;'>Comment Results:</h2><ul style='list-style:none;'>"

    for comment_text in comments:
        data = {
            "comment_text": comment_text
        }
        try:
            res = requests.post(post_url, headers=headers, data=data)
            if res.status_code == 200:
                result_html += f"<li style='color:lime;'>✔️ सही: {comment_text}</li>"
            else:
                result_html += f"<li style='color:red;'>❌ गलत: {comment_text}</li>"
        except Exception as e:
            result_html += f"<li style='color:red;'>❌ Error: {comment_text} - {e}</li>"
        time.sleep(delay)

    result_html += "</ul>"
    return result_html

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
