from flask import Flask, request, render_template_string
import requests
import time
import random
import threading

app = Flask(__name__)

# ✅ 20+ User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X)",
    "Mozilla/5.0 (Android 9; SM-A107F)",
    "Mozilla/5.0 (Linux; Android 11; M2101K6G)",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0)",
    "Mozilla/5.0 (Windows NT 10.0; ARM64)",
    "Mozilla/5.0 (Linux; Android 12; Pixel 4a)",
    "Mozilla/5.0 (Linux; Android 7.0; Nexus 5X)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    "Mozilla/5.0 (Linux; Android 8.1.0; Redmi 6A)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64)",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 10; Infinix X650C)",
    "Mozilla/5.0 (Linux; Android 13; Samsung Galaxy A54)"
]

EMOJIS = ["😊", "🔥", "👍", "💯", "✔️", "🚀", "❤️", "😂", "🙏", "🥳", "😎", "🌟", "💥", "😇"]

HTML_FORM = '''
<html>
    <head><title>Facebook Auto Comment</title></head>
    <body style="background-color:black; color:white;">
        <h2>Facebook Auto Comment (Multi-Token Handling)</h2>
        <form action="/submit" method="post" enctype="multipart/form-data">
            Token File: <input type="file" name="token_file" required><br>
            Comment File: <input type="file" name="comment_file" required><br>
            Post URL: <input type="text" name="post_url" required><br>
            Interval (Seconds): <input type="number" name="interval" value="400" required><br>
            <input type="submit" value="Start Commenting">
        </form>
        <br>
        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
    </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    token_file = request.files['token_file']
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = token_file.read().decode('utf-8').splitlines()
    comments = comment_file.read().decode('utf-8').splitlines()

    if not tokens or not comments:
        return render_template_string(HTML_FORM, message="❌ Token या Comment File खाली है!")

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    blocked_tokens = set()
    last_user_agent_time = time.time()
    current_user_agent = random.choice(USER_AGENTS)

    def post_comment(token, comment):
        nonlocal current_user_agent, last_user_agent_time

        # ✅ Every 26 mins, rotate User-Agent
        if time.time() - last_user_agent_time > 1560:
            current_user_agent = random.choice(USER_AGENTS)
            last_user_agent_time = time.time()

        headers = {"User-Agent": current_user_agent}
        payload = {'message': comment, 'access_token': token}
        try:
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                print(f"✅ Comment Success: {comment}")
                return True
            elif "error" in response.json() and "OAuthException" in response.text:
                blocked_tokens.add(token)
                print(f"❌ Blocked Token: {token[:10]}...")
                return False
            else:
                print(f"❌ Comment Failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def start_commenting():
        index = 0
        while True:
            active_tokens = [t for t in tokens if t not in blocked_tokens]
            if not active_tokens:
                print("❌ All Tokens Blocked! Retrying all in 30 minutes...")
                time.sleep(1800)
                blocked_tokens.clear()
                continue

            token = active_tokens[index % len(active_tokens)]
            comment = comments[index % len(comments)]
            emoji = random.choice(EMOJIS)
            final_comment = f"{comment} {emoji}"

            post_comment(token, final_comment)
            index += 1
            time.sleep(interval + random.randint(5, 20))

    threading.Thread(target=start_commenting, daemon=True).start()
    return render_template_string(HTML_FORM, message="✅ Commenting Started!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
