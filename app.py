from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os
import uuid
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comfort.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), unique=True, nullable=False)
    retry_count = db.Column(db.Integer, default=0)
    last_prompt = db.Column(db.Text)
    last_response = db.Column(db.Text)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-4-maverick:free"
# MODEL = "meta-llama/llama-3-70b-instruct"

# retry_count = {}  # 儲存每位使用者的錯誤反應次數（暫時簡化為全域）

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_comfort", methods=["POST"])
def get_comfort():
    data = request.get_json()
    prompt = data.get("prompt", "")
    feedback = data.get("feedback", "")  # 接收回饋（謝謝你/爛透了）
    response_text = "..."

    # 根據使用者 IP 區分用戶
    # user_id = request.headers.get("User-Agent") + request.remote_addr or "default"
     # 嘗試從 cookie 取得 user_id，如果沒有就產生一個新的
    user_id = request.cookies.get("user_id")
    new_cookie = False

    if not user_id:
        user_id = str(uuid.uuid4())
        new_cookie = True 
        
    print("user_id：", user_id)

    # count = retry_count.get(user_id, 0)

    response_data = None

    # 從資料庫中取得使用者狀態
    user_state = UserState.query.filter_by(user_id=user_id).first()
    if not user_state:
        user_state = UserState(user_id=user_id)
        db.session.add(user_state)
        db.session.commit()

    # 回饋處理
    if feedback == "謝謝妳":
        user_state.retry_count = 0
        # retry_count[user_id] = 0  # 重置次數
        # retry_count["count"] = 0
        response_data = {
            "response": "😺 謝謝你願意說出來～",
            "gray_cat_image": "cat2.webp"  # 讓灰貓變得更可愛地回應
        }
    
    elif feedback == "爛透了":
        user_state.retry_count += 1
        # retry_count.setdefault("count", 0)
        # retry_count["count"] += 1
        # count += 1
        # retry_count[user_id] = count

        # if count >= 3:
        #     retry_count[user_id] = 0
        if user_state.retry_count >= 3:
            user_state.retry_count = 0
            response_data = {
                "response": "⚠️ 白貓安慰失敗…已經不再說話，只是靜靜陪著你。",
                "cat_image": "cat11.webp",  # 表示白貓圖要換
                "allow_feedback": False
            }

    db.session.commit() 

    if response_data:
        res = jsonify(response_data)
        if new_cookie:
            res.set_cookie("user_id", user_id, max_age=60*60*24*30)
        return res
   

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一隻擅長安慰人的貓咪，請用溫柔、有層次的語氣簡短回應使用者的煩惱。"},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    res = requests.post(API_URL, json=payload, headers=headers)
    try:
        res.raise_for_status()
        json_response = res.json()
        if "choices" not in json_response:
            raise ValueError(f"API 回傳格式錯誤：{json_response}")
        response_text = json_response["choices"][0]["message"]["content"]
        # 儲存對話到資料庫
        user_state.last_prompt = prompt
        user_state.last_response = response_text
        db.session.commit()
    except Exception as e:
        print("❌ 回傳錯誤：", res.status_code)
        print("❌ 回傳內容：", res.text)
        return jsonify({
            "response": "⚠️ 貓咪暫時累了，稍後再說好嗎？"
        })

    res = jsonify({
        "response": response_text,
        "cat_image": "cat1.webp"  # 預設白貓圖
    })
    if new_cookie:
        res.set_cookie("user_id", user_id, max_age=60*60*24*30)  # 存一個月
    return res

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

