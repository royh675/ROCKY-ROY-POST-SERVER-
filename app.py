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
        input, button {
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
        <form action="/start_commenting" method="post" enctype="multipart/form-data">
            <input type="file" name="cookies" required><br>
            <input type="file" name="comments" required><br>
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
    cookies_file = request.files['cookies']
    comments_file = request.files['comments']
    post_url = request.form['post_url']
    delay = int(request.form['delay'])

    cookies = cookies_file.read().decode().splitlines()
    comments = comments_file.read().decode().splitlines()

    success = 0

    for cookie in cookies:
        for comment in comments:
            headers = {
                "cookie": cookie,
                "user-agent": "Mozilla/5.0"
            }
            data = {
                "comment_text": comment
            }

            try:
                res = requests.post(post_url, headers=headers, data=data)
                if res.status_code == 200:
                    success += 1
                time.sleep(delay)
            except Exception as e:
                print("Error:", e)

    return f"<h2 style='color:lime;'>Done! Total comments sent: {success}</h2>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
