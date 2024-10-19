from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


app = Flask(__name__)
DB = "books.sqlite"


def get_db():
    if "books" not in g:
        g.db = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/books", methods=["GET", "POST"])
def books():
    db = get_db()
    if request.method == "POST":
        isbn = request.form.get("isbn")
        author = request.form.get("author")
        title = request.form.get("title")
        year = request.form.get("year")
        publisher = request.form.get("publisher")
        db.execute(
            "INSERT INTO books (isbn, author, title, year, publisher) VALUES (?,?,?,?,?)",
            (isbn, author, title, year, publisher),
        )
        db.commit()
        return redirect(url_for("books"))
    if request.method == "GET":
        books = db.execute("SELECT * FROM books").fetchall()
        members = db.execute("SELECT * FROM members").fetchall()
        return render_template("books.html", books=books, members=members)
    return render_template("books.html")


@app.route("/members", methods=["GET", "POST"])
def members():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name")
        neptun = request.form.get("neptun")
        db.execute(
            "INSERT INTO members (name, neptun) VALUES (?,?)",
            (name, neptun),
        )
        db.commit()
        return redirect(url_for("members"))
    if request.method == "GET":
        members = db.execute("SELECT * FROM members").fetchall()
        return render_template("members.html", members=members)
    return render_template("members.html")


@app.route("/borrow", methods=["POST"])
def borrow():
    db = get_db()
    book_id = request.form.get("id")
    member_neptun = request.form.get("neptun")
    member_name = db.execute(
        "SELECT name FROM members WHERE neptun=?", (member_neptun,)
    ).fetchone()
    db.execute(
        "UPDATE books SET is_borrowed=1, borrower=(?), score=score+1 WHERE id=(?)",
        (
            member_name["name"],
            book_id,
        ),
    )
    db.execute("UPDATE members SET score=score+1 WHERE neptun=?", (member_neptun,))
    db.commit()
    return redirect(url_for("books"))


@app.route("/unborrow", methods=["POST"])
def unborrow():
    db = get_db()
    book_id = request.form.get("id")
    db.execute("UPDATE books SET is_borrowed=0, borrower=NULL WHERE id=?", (book_id,))
    db.commit()
    return redirect(url_for("books"))


@app.route("/stats")
def stats():
    db = get_db()
    score_by_books = db.execute(
        "SELECT title, score FROM books WHERE score>0"
    ).fetchall()
    score_by_members = db.execute(
        "SELECT name, score FROM members WHERE score>0"
    ).fetchall()

    plt.bar(
        [item["title"] for item in score_by_books],
        [item["score"] for item in score_by_books],
    )
    plt.savefig("static/images/score_by_books.png")
    plt.close()

    plt.bar(
        [item["name"] for item in score_by_members],
        [item["score"] for item in score_by_members],
    )
    plt.savefig("static/images/score_by_members.png")
    plt.close()

    return render_template("stats.html")


if __name__ == "__main__":
    app.teardown_appcontext(close_db)
    app.run(port=8000, debug=True, host="0.0.0.0")
