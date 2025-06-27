from datetime import datetime
from flask import Flask, flash, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from helpers import login_required

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'super-secret-key'
Session(app)

def get_db():
    conn = sqlite3.connect("study-smart.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.")
            return redirect("/login")
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["hash"], password):
            flash("Invalid username or password.")
            return redirect("/login")
        flash("Logged in successfully.")
        session["user_id"] = user["id"]
        return redirect('/')
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect("/login")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            flash("All fields are required.")
            return redirect("/register")
        
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect("/register")

        db = get_db()
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            flash("Username already exists.")
            return redirect("/register")

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        flash("Registered successfully. Please log in.")
        return redirect("/login")
    
    return render_template("register.html")

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    user_id = session["user_id"]
    
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()

    sessions = db.execute("SELECT date, SUM(duration) as total_minutes FROM study_sessions WHERE user_id = ? GROUP BY date ORDER BY date DESC", (user_id,)).fetchall()
    labels = [row["date"] for row in sessions]
    values = [row["total_minutes"] for row in sessions]

    return render_template("dashboard.html", tasks=tasks, labels=labels, values=values)

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")

        if not title:
            flash("Task title is required.", "danger")
            return redirect("/tasks")
        
        db.execute("INSERT INTO tasks (user_id, title, description, due_date, priority) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, title, description, due_date, priority))
        db.commit()
        flash("Task added successfully.", "success")
        return redirect("/tasks")

    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC", (user_id,)).fetchall()
    return render_template("tasks.html", tasks=tasks)


@app.route("/timer")
@login_required
def timer():
    return render_template("timer.html")

@app.route("/log_session", methods=["POST"])
@login_required
def log_session():
    db = get_db()
    user_id = session["user_id"]
    today = datetime.now().strftime("%Y-%m-%d")

    db.execute("INSERT INTO study_sessions (user_id, date, duration) VALUES (?, ?, ?)", (user_id, today, 25),)
    db.commit()

    return "", 204

@app.route("/complete_task", methods=["POST"])
@login_required
def complete_task():
    db = get_db()
    user_id = session["user_id"]
    task_id = request.form.get("task_id")
    db.execute("UPDATE tasks SET complete = 1 WHERE id = ? AND user_id = ?", (task_id, user_id))
    db.commit()
    flash("Task marked as complete.", "success")
    return redirect("/tasks")