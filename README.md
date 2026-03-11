# 🎓 Gurunanak University — AI College Chatbot

A full-stack AI chatbot deployable on **Vercel**, **Render**, **Railway**, or **locally**.

---

## 📁 Project Structure

```
college-chatbot/
├── app.py                  ← Flask backend (single entry point)
├── requirements.txt        ← Python dependencies
├── Procfile                ← For Render / Heroku
├── vercel.json             ← For Vercel
├── railway.json            ← For Railway
├── render.yaml             ← For Render
├── .gitignore
├── data/
│   └── college_data.json   ← Intent & response dataset
└── public/
    └── index.html          ← Frontend (served by Flask)
```

---

## 🚀 Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open in browser
# http://localhost:5000
```

---

## 🐙 Push to GitHub

```bash
# 1. Initialize git (inside the project folder)
git init
git add .
git commit -m "Initial commit - College Chatbot"

# 2. Create a repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/college-chatbot.git
git branch -M main
git push -u origin main
```

---

## ▲ Deploy on Vercel (Free)

1. Push to GitHub (steps above)
2. Go to → https://vercel.com
3. Click **"Add New Project"**
4. Import your GitHub repo
5. Vercel auto-detects `vercel.json` — click **Deploy**
6. Your live URL: `https://college-chatbot-xxx.vercel.app`

> ⚠️ Note: Vercel's free tier has a 10s timeout for Python. For production use Render or Railway.

---

## 🟣 Deploy on Render (Recommended — Free)

1. Push to GitHub
2. Go to → https://render.com
3. Click **"New Web Service"**
4. Connect your GitHub repo
5. Settings auto-filled from `render.yaml`:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click **Deploy** → Live in ~2 minutes
7. Your live URL: `https://college-chatbot.onrender.com`

---

## 🚂 Deploy on Railway (Free Tier)

1. Push to GitHub
2. Go to → https://railway.app
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repo — Railway reads `railway.json` automatically
5. Click **Deploy**
6. Your live URL: `https://college-chatbot.up.railway.app`

---

## 🌐 API Endpoints

| Method | Endpoint        | Description                  |
|--------|-----------------|------------------------------|
| GET    | `/`             | Serves the frontend UI       |
| POST   | `/api/chat`     | Send message, get response   |
| GET    | `/api/intents`  | List all loaded intents      |
| POST   | `/api/intents`  | Add a new intent dynamically |
| GET    | `/api/health`   | Health check                 |

### POST /api/chat — Example

**Request:**
```json
{ "message": "What courses do you offer?" }
```

**Response:**
```json
{
  "response": "Courses Offered at Greenfield University...",
  "intent": "courses",
  "confidence": 0.584
}
```

---

## ✏️ Add New Q&A Topics

Edit `data/college_data.json`:

```json
{
  "tag": "clubs",
  "patterns": ["student clubs", "extracurricular", "activities", "societies"],
  "responses": ["We have 40+ student clubs covering tech, arts, sports, and culture!"]
}
```

Or use the live API (no restart needed):

```bash
curl -X POST https://your-app.onrender.com/api/intents \
  -H "Content-Type: application/json" \
  -d '{"tag":"clubs","patterns":["clubs","activities"],"responses":["We have 40+ clubs!"]}'
```

---

## 🛠️ Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3.11, Flask, Gunicorn        |
| NLP      | Custom TF-IDF cosine similarity     |
| Data     | JSON (easily swap to SQLite/MongoDB)|
| Frontend | HTML · CSS · Vanilla JavaScript     |
| Deploy   | Vercel · Render · Railway · Local   |

---

## 📝 License

MIT — free to use and modify for educational purposes.







my project live URL: https://ai-chatbot-for-college-information-system.onrender.com
