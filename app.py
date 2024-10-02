from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import re
from datetime import datetime
import os
import platform

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
    return render_template("index.html", message=message)


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
