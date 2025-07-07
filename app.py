from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

TASK_FILE = "tasks.json"
USER_FILE = "users.json"
DIARY_FOLDER = 'diaries'

# ---------- Utility Functions ----------

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def get_today():
    return datetime.today().strftime('%Y-%m-%d')

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

# 🌟 Motivational Quotes
QUOTES = [
    "✨ Stay focused and never give up!",
    "💪 You’ve got this!",
    "🌟 One step at a time.",
    "🚀 Keep pushing forward!",
    "📌 Progress over perfection!",
    "🌈 Every day is a fresh start!"
]

@app.route('/')
@login_required
def index():
    today = get_today()
    all_tasks = load_tasks()
    today_tasks = [t for t in all_tasks if t['date'] == today and t['user'] == session['user']]
    quote = random.choice(QUOTES)
    total = len(today_tasks)
    completed = sum(1 for t in today_tasks if t['status'] == 'Completed')
    progress = f"{completed}/{total} completed" if total else "No tasks yet"
    return render_template('index.html', tasks=today_tasks, quote=quote, progress=progress)

@app.route('/all_tasks')
@login_required
def all_tasks():
    all_tasks = load_tasks()
    user_tasks = [t for t in all_tasks if t['user'] == session['user']]
    return render_template('all_tasks.html', tasks=user_tasks)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        time = datetime.strptime(request.form['time'], "%H:%M").strftime("%I:%M %p")
        date = request.form['date']
        priority = request.form['priority']

        new_task = {
            "title": title,
            "time": time,
            "date": date,
            "priority": priority,
            "status": "Pending",
            "user": session['user']
        }

        tasks = load_tasks()
        tasks.append(new_task)
        save_tasks(tasks)
        return redirect(url_for('index'))

    return render_template('add_task.html')

@app.route('/complete/<int:task_index>')
@login_required
def complete_task(task_index):
    tasks = load_tasks()
    user_tasks = [t for t in tasks if t['user'] == session['user']]
    if 0 <= task_index < len(user_tasks):
        for i, task in enumerate(tasks):
            if task['user'] == session['user'] and task == user_tasks[task_index]:
                tasks[i]['status'] = 'Completed'
                break
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_index>')
@login_required
def delete_task(task_index):
    tasks = load_tasks()
    user_tasks = [t for t in tasks if t['user'] == session['user']]
    if 0 <= task_index < len(user_tasks):
        original_task = user_tasks[task_index]
        tasks = [t for t in tasks if t != original_task]
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    if request.method == 'POST':
        entry = request.form['entry']
        today = get_today()
        os.makedirs(DIARY_FOLDER, exist_ok=True)
        diary_file = f'diary_{session["user"]}_{today}.txt'
        with open(os.path.join(DIARY_FOLDER, diary_file), 'w') as f:
            f.write(entry)
        return redirect(url_for('index'))
    return render_template('diary.html')

@app.route('/diaries')
@login_required
def list_diaries():
    user = session['user']
    diary_entries = []

    if os.path.exists(DIARY_FOLDER):
        for filename in os.listdir(DIARY_FOLDER):
            if filename.startswith(f'diary_{user}_') and filename.endswith('.txt'):
                filepath = os.path.join(DIARY_FOLDER, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    title_line = content.splitlines()[0] if content else "Untitled"
                    preview = content[:100] + "..." if len(content) > 100 else content
                date_part = filename.replace(f'diary_{user}_', '').replace('.txt', '')
                diary_entries.append({
                    'filename': filename,
                    'date': date_part,
                    'title': title_line.strip(),
                    'preview': preview.strip()
                })

    diary_entries.sort(key=lambda x: x['date'], reverse=True)
    return render_template('diary_list.html', diaries=diary_entries)

@app.route('/diary/<filename>')
@login_required
def view_diary(filename):
    path = os.path.join(DIARY_FOLDER, filename)
    if not os.path.exists(path):
        flash("Diary entry not found")
        return redirect(url_for('list_diaries'))
    with open(path, 'r') as f:
        content = f.read()
    return render_template('view_diary.html', content=content, filename=filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for uid, user in users.items():
            if user['name'] == username and user['password'] == password:
                session['user'] = username
                return redirect(url_for('index'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users.values():
            if user['name'] == username:
                flash('⚠️ Username already exists!')
                return redirect(url_for('register'))
        user_id = str(len(users) + 1)
        users[user_id] = {"name": username, "password": password}
        save_users(users)
        flash('✅ Registered successfully! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
