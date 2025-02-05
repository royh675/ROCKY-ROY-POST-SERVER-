PK     Y@EZ�0���  �     app.pyimport os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to post a comment on Facebook
def post_comment(token, post_url, comment):
    post_id = post_url.split('/')[-1]
    api_url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {'message': comment, 'access_token': token}
    response = requests.post(api_url, data=payload)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form['token']
        username = request.form['username']
        post_url = request.form['post_url']
        time_interval = request.form['time_interval']
        comment_text = request.form['comment_text']
        
        with open('token.txt', 'w') as f:
            f.write(token)
        with open('file.txt', 'w') as f:
            f.write(username)
        with open('post_url.txt', 'w') as f:
            f.write(post_url)
        with open('time.txt', 'w') as f:
            f.write(time_interval)
        with open('comment.txt', 'w') as f:
            f.write(comment_text)

        # Posting a comment
        response = post_comment(token, post_url, comment_text)
        return render_template('index.html', message="Comment Posted!", response=response)

    return render_template('index.html', message=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)PK     Y@EZ��0�         requirements.txtFlask
requestsPK     J?EZ            	   token.txtPK     J?EZ               file.txtPK     J?EZ               post_url.txtPK     J?EZ               time.txtPK     Y@EZDƑs         Procfileweb: python app.pyPK     8@EZ               comment.txtPK     Y@EZ�(��  �     templates/index.html<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Auto Comment Bot</title>
</head>
<body>
    <h1>Facebook Auto Comment Bot</h1>
    {% if message %}
        <p style="color:green;">{{ message }}</p>
    {% endif %}
    <form method="POST">
        <label>Access Token:</label><br>
        <input type="text" name="token" required><br><br>
        
        <label>Username:</label><br>
        <input type="text" name="username" required><br><br>
        
        <label>Post URL:</label><br>
        <input type="text" name="post_url" required><br><br>
        
        <label>Time Interval (seconds):</label><br>
        <input type="number" name="time_interval" required><br><br>
        
        <label>Comment Text:</label><br>
        <input type="text" name="comment_text" required><br><br>

        <input type="submit" value="Post Comment">
    </form>
</body>
</html>PK     Y@EZ�0���  �             ��    app.pyPK     Y@EZ��0�                 ���  requirements.txtPK     J?EZ            	           ��+  token.txtPK     J?EZ                       ��R  file.txtPK     J?EZ                       ��x  post_url.txtPK     J?EZ                       ���  time.txtPK     Y@EZDƑs                 ���  ProcfilePK     8@EZ                       ��   comment.txtPK     Y@EZ�(��  �             ��)  templates/index.htmlPK    	 	    8    