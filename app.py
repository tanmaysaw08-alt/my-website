
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "submissions.db"


def setup_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/bca-first-semester")
def bca_first_semester():
    return render_template("bca_first_semester.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not phone:
        return "Name and phone are required.", 400

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        INSERT INTO submissions
        (name, phone, email, message)
        VALUES (?, ?, ?, ?)
        """,
        (name, phone, email, message)
    )

    conn.commit()
    conn.close()

    return render_template("success.html", name=name)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password", "")

        if password != "1234":
            return render_template(
                "admin.html",
                error="Wrong password"
            )

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        submissions = conn.execute(
            "SELECT * FROM submissions ORDER BY id DESC"
        ).fetchall()

        conn.close()

        return render_template(
            "dashboard.html",
            submissions=submissions
        )

    return render_template("admin.html")


setup_database()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
```
