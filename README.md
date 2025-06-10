# 🐾 Comforting Cat

**Comforting Cat** is a gentle and healing web application. Whenever you're feeling anxious or low, you can talk to the cat. It will reply with soothing and nuanced words. If you're not satisfied with the response, the cat will try again — up to three times. After that, it will quietly stay with you.

---

## 🌟 Features

- Uses a Large Language Model (LLM) via OpenRouter API to respond to user input
- Allows up to 3 retries when the user selects “That was terrible”
- Tracks users with cookies (UUID) for session distinction
- Stores user interaction state with SQLite
- Supports user feedback: “Thanks” or “Sucks”
- Cat image changes depending on feedback (white cat ↔ gray cat)

---

## 📁 Project Structure

```
comforting-cat/
├── app.py # Main Flask application
├── requirements.txt # List of dependencies
├── templates/
│ └── index.html # Frontend (includes animation and logic)
├── static/
│ └── cat1.webp # White cat image (can be replaced)
├── instance/
│ └── comfort.db # SQLite database (auto-generated on startup)
├── .env # API key configuration (user-provided)
├── .gitignore # Ignores venv, .env, and DB files
└── venv/ # Python virtual environment
```

---

## 🚀 Installation & Running the App

1. **Clone the project**

```bash
git clone https://github.com/yourname/comforting-cat.git
cd comforting-cat
```

2. **Create and activate a virtual environment**
   
```bash
python3 -m venv venv
source venv/bin/activate
```
For future use, you only need to run source venv/bin/activate.


3. **Install dependencies**

```bash
pip install -r requirements.txt
```


4. **Add a .env file with your OpenRouter API key**

```bash
OPENROUTER_API_KEY=your_api_key_here
```

5. **Start the application**

```bash
python app.py
```

Then visit http://127.0.0.1:5000 to start chatting.

On first launch, instance/comfort.db will be created automatically.

---

## 🧠 How It Works
### ✅ User Identification
* A UUID is saved to cookies to identify each user

The session remains unique across devices and visits

### ✅ Database Table: user_state
| Column          | Description                         |
| --------------- | ----------------------------------- |
| `user_id`       | Unique identifier for the user      |
| `retry_count`   | Number of remaining retries (max 3) |
| `last_prompt`   | Last user input                     |
| `last_response` | Last system reply                   |

### ✅ Comforting Logic

1. User types a message

2. The prompt is sent to the OpenRouter API (Llama4 Maverick model)

3. The system replies with comforting text (default: cat1.webp)

4. If user clicks Thanks → retries reset → cat thanks the user

5. If user clicks Sucks → retry count +1 → another response is given

6. After 3 failed attempts → final message shown (image switches to cat11.webp), feedback buttons disappear

---

## 🗃️ Viewing the Database (Developer Use)
If you'd like to inspect user records stored in the SQLite database, use the following:

```bash
sqlite3 instance/comfort.db
```

Inside the SQLite shell:

```bash
.tables         -- View available tables
.headers on     -- Show column names
.mode column    -- Format columns neatly
SELECT * FROM user_state;
.quit           -- Exit SQLite shell
```
---

## ⚙️ Deployment Notes (Example: GCP VM)

1. Install Python and required tools on the VM

2. Run: `python3 -m venv venv && source venv/bin/activate`

3. Install dependencies: `pip install -r requirements.txt`

4. Set up a systemd service to run the app
   Use gunicorn + nginx for production environments (see deploy.sh as a reference)

5. WebSite：http://34.29.177.247/

---

## 📬 Contact & Roadmap

* Add language toggle (English / Chinese)
* Track emotional state over time via feedback
* Let users collect their favorite comforting replies

If you'd like to help this cat comfort more people, feel free to fork the project or send a pull request 🐱
