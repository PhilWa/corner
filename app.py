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

    news_items = read_news_from_tsv()
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


def read_news_from_tsv():
    News = namedtuple("News", ["id", "date", "content", "misc", "to_pod", "to_post"])
    news_items = []
    with open("news.tsv", "r", encoding="utf-8") as tsv_file:
        reader = csv.reader(tsv_file, delimiter="|")
        next(reader)  # Skip header row
        for row in reader:
            # Unescape newlines in content
            row[2] = row[2].replace("\\n", "\n")
            # Ensure we have all fields, use empty strings if missing
            row += [""] * (6 - len(row))
            news_items.append(News(*row[:6]))  # Only use the first 6 fields
    return sorted(news_items, key=lambda x: x.date, reverse=True)[
        :3
    ]  # Return latest 3 items


articles = [
    {
        "id": 1,
        "title": "The Future of AI in Switzerland",
        "excerpt": "Exploring the rapidly evolving AI landscape in Switzerland, including key players, research initiatives, and potential impacts on various industries.",
        # "image_url": url_for("static", filename="images/ai_switzerland.jpg"),
        "date": "May 15, 2023",
        "author": "John Doe",
    },
    {
        "id": 2,
        "title": "Swiss Fintech Revolution",
        "excerpt": "An in-depth look at how fintech startups are reshaping the Swiss financial sector, from blockchain applications to innovative payment solutions.",
        # "image_url": url_for("static", filename="images/fintech_swiss.jpg"),
        "date": "May 10, 2023",
        "author": "Jane Smith",
    },
    # Add more articles as needed
]


@app.route("/article/<int:article_id>")
def article(article_id):
    # Fetch the article from the list of articles
    article = next((a for a in articles if a["id"] == article_id), None)
    if article is None:
        os.abort(404)
    return render_template("article.html", article=article)


@app.route("/deep-dives")
def deep_dives():
    return render_template("deep_dives.html", articles=articles)


@app.route("/conditional-relation-extraction")
def conditional_relation_extraction():
    return render_template("conditional_relation_extraction.html")


@app.route("/rag-architecture")
def rag_architecture():
    return render_template("rag_architecture.html")


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
