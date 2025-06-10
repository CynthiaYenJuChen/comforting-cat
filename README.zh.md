# 🐾 安心語貓咪（Comforting Cat）

這是一個簡單的療癒系 Web 應用，當你覺得煩惱、心情低落時，可以向貓咪傾訴，它會用溫柔、富有層次的語氣回應你。如果你對安慰不滿意，它還能嘗試再安慰你幾次，直到三次機會用完。

---

## 🌟 功能介紹

* 使用 LLM 回應使用者的煩惱（OpenRouter API）
* 三次「That was terrible」機會後，白貓會停止說話
* Cookie 儲存使用者 ID，讓不同裝置可分辨身份
* 使用 SQLite 儲存使用者對話狀態
* 提供使用者對白貓的反饋（Thanks / Sucks）
* 回饋後切換圖片（白貓與灰貓）

---

## 📁 專案結構

```
comforting-cat/
├── app.py                 # 主應用程式（Flask）
├── requirements.txt       # 所需套件列表
├── templates/
│   └── index.html         # 前端頁面（含動畫邏輯）
├── static/
│   └── cat1.webp          # 白貓圖片（可替換）
├── instance/
│   └── comfort.db         # SQLite 資料庫（啟動時自動建立）
├── .env                   # API 金鑰（需自行設定）
├── .gitignore             # 忽略 venv、.env 與 db 等檔案
└── venv/                  # 虛擬環境
```

---

## 🚀 安裝與啟動

1. **Clone 專案**

```bash
git clone https://github.com/yourname/comforting-cat.git
cd comforting-cat
```

2. **建立虛擬環境並啟動**
  未來若只有啟動，僅需跑source那行
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **安裝依賴套件**

```bash
pip install -r requirements.txt
```

4. **新增 `.env` 檔案並加入 OpenRouter 金鑰**

```
OPENROUTER_API_KEY=你的API金鑰
```

5. **執行應用程式**

```bash
python app.py
```

然後瀏覽 [http://127.0.0.1:5000](http://127.0.0.1:5000) 開始聊天。

> 初次啟動時會自動建立 `instance/comfort.db`。

---

## 🧠 系統邏輯說明

### ✅ 使用者分辨（user\_id）

* 透過 Cookie 儲存 UUID，如果不存在就新建

### ✅ 資料庫紀錄內容（user\_state 表）

| 欄位             | 說明                |
| -------------- | ----------------- |
| user\_id       | 使用者 ID（UUID）      |
| retry\_count   | 貓咪還可安慰的次數（最多 3 次） |
| last\_prompt   | 上一次使用者輸入          |
| last\_response | 上一次系統回覆           |

### ✅ 安慰流程

1. 使用者輸入 prompt
2. 傳給 OpenRouter（Llama4 Maverick）模型
3. 回傳後顯示白貓安慰語句（預設圖片為 `cat1.webp`）
4. 使用者若回應 Thanks ➜ 重置次數 ➜ 白貓回應感謝語
5. 使用者若回應 Sucks ➜ retry 次數 +1 ➜ 嘗試安慰
6. 第三次後會回應結束語（`cat11.webp`）並關閉回饋按鈕

---
## 🗃️ 查看資料庫內容（開發用）
若你想檢查記錄在資料庫中的使用者對話狀態，可使用 SQLite CLI：

```bash
sqlite3 instance/comfort.db
```
進入後輸入以下指令：

```bash
.tables           -- 查看資料表
.headers on       -- 顯示欄位名稱
.mode column      -- 美化對齊格式
SELECT * FROM user_state;
.quit             -- 離開 SQLite CLI
```
---

## ⚙️ 部署建議（GCP VM）

1. 安裝 Python 與必要依賴
2. 跑 `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. 使用 `systemd` 建立服務，搭配 Gunicorn + Nginx 可做正式部署（見 `deploy.sh` 示意）
5. 網址：http://34.29.177.247/

---

## 📬 聯絡作者 / 未來規劃

* 新增貓咪語系切換（中英）
* 回饋記錄與情緒追蹤（分析使用者狀態）
* 收藏安心語卡片功能

---

如果你也想讓貓咪安慰更多人，歡迎 fork 或貢獻 pull request 🐱
