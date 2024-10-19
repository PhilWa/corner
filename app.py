from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import re
from datetime import datetime
import os
import platform
from collections import namedtuple
import csv

app = Flask(__name__)


# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("emails.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


init_db()

# Email validation regex
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        email = request.form.get("email")
        if not EMAIL_REGEX.match(email):
            message = "Email format is not as expected."
        else:
            try:
                conn = sqlite3.connect("emails.db")
                c = conn.cursor()
                c.execute("INSERT INTO emails (email) VALUES (?)", (email,))
                conn.commit()
                conn.close()
                message = "Email saved successfully!"
            except sqlite3.IntegrityError:
                message = "This email is already registered."

    news_items = get_latest_news()
    return render_template("index.html", message=message, news_items=news_items)


@app.route("/toggle_cells", methods=["POST"])
def toggle_cells():
    data = request.get_json()
    x = data["x"]
    y = data["y"]
    toggle_positions = get_cells_to_toggle(x, y)

    # Ensure the clicked cell is always toggled
    toggle_positions.append((x, y))

    return jsonify({"toggle_cells": toggle_positions})


def get_cells_to_toggle(x, y):
    import random

    positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    random_cells = random.sample(positions, 5)
    toggle_positions = [(x + dx, y + dy) for dx, dy in random_cells]
    return toggle_positions


def get_latest_news():
    news_dir = os.path.join(app.root_path, "templates", "news")
    html_files = [f for f in os.listdir(news_dir) if f.endswith(".html")]
    html_files.sort(
        key=lambda x: os.path.getmtime(os.path.join(news_dir, x)), reverse=True
    )
    latest_files = html_files[:3]

    news_items = []
    for filename in latest_files:
        file_path = os.path.join(news_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        mod_time = os.path.getmtime(file_path)
        upload_date = datetime.fromtimestamp(mod_time).strftime("%B %d, %Y")

        # Check if the file is a podcast (you might want to implement your own logic here)
        is_podcast = True

        news_items.append(
            {"upload_date": upload_date, "content": content, "is_podcast": is_podcast}
        )
    return news_items


@app.route("/conditional-relation-extraction")
def conditional_relation_extraction():
    return render_template("conditional_relation_extraction.html")


@app.route("/rag-architecture")
def rag_architecture():
    return render_template("rag_architecture.html")


@app.route("/watson")
def watson():
    return render_template("watson.html")


@app.route("/swift")
def swift():
    return render_template("swift.html")


if __name__ == "__main__":
    is_mac = platform.system() == "Darwin"
    is_production = os.environ.get("PRODUCTION", "false").lower() == "true"

    if is_mac and not is_production:
        # Running on Mac in development mode
        app.run(debug=True)
    else:
        # Running in production or non-Mac environment
        from flup.server.fcgi import WSGIServer

        WSGIServer(app).run()
