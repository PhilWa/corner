import sqlite3


def add_sample_articles():
    conn = sqlite3.connect("corner.db")
    c = conn.cursor()
    articles = [
        (
            "Swiss AI Startup Raises $10M",
            "A promising AI startup from Zurich has secured $10 million in Series A funding...",
            "2023-05-01",
        ),
        (
            "New Tech Hub Opens in Geneva",
            "Geneva welcomes a new state-of-the-art tech hub, fostering innovation and collaboration...",
            "2023-05-05",
        ),
        (
            "Blockchain Revolution in Swiss Banking",
            "Swiss banks are adopting blockchain technology to streamline operations and enhance security...",
            "2023-05-10",
        ),
    ]
    c.executemany(
        "INSERT INTO articles (title, content, date) VALUES (?, ?, ?)", articles
    )
    conn.commit()
    conn.close()
