# 🧠 DayWise – Be Wise With Your Day

**DayWise** is a simple, elegant personal productivity web app built using **Flask**. It helps you manage daily tasks, write diary entries, track your progress, and stay motivated with quotes — all in one place.

---

## 🚀 Features

- ✅ Add, complete, and delete daily tasks  
- 📅 View all tasks or just today’s  
- 📈 Task progress tracking  
- 📔 Personal diary writing  
- 📂 View archive of past diary entries  
- 💬 Daily motivational quote  
- 🔐 User authentication (Login/Register)


daywise/
│
├── templates/              # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── add_task.html
│   ├── all_tasks.html
│   ├── diary.html
│   ├── diary_list.html
│   └── view_diary.html
│
├── static/                 # (Optional) CSS/JS files
│
├── app.py                  # Main Flask app
├── tasks.json              # Task data (auto-generated)
├── users.json              # User data (auto-generated)
├── diaries/                # Diary entries folder (auto-created)
└── requirements.txt        # Python dependencies


## 🖥️ Tech Stack

- Python 3.x  
- Flask  
- HTML + Bootstrap (UI)  
- JSON (for data storage)


## 🔧 How to Run Locally

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/daywise.git
   cd daywise

python -m venv venv
source venv/bin/activate      # On Linux/macOS
venv\Scripts\activate         # On Windows

pip install -r requirements.txt

python app.py
http://127.0.0.1:5000/
