from flask import Flask, render_template, redirect, url_for, request
from config import Config
from models import db, User, Book, Loan
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- AUTH ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"],
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ---------------- BOOKS ----------------

@app.route("/books")
@login_required
def books():
    query = Book.query

    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")

    if title:
        query = query.filter(Book.title.contains(title))
    if author:
        query = query.filter(Book.author.contains(author))
    if genre:
        query = query.filter(Book.genre.contains(genre))

    books = query.all()
    return render_template("books.html", books=books)

@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if current_user.role != "admin":
        return "Access Denied"

    if request.method == "POST":
        book = Book(
            title=request.form["title"],
            author=request.form["author"],
            genre=request.form["genre"],
            year=request.form["year"],
            copies=request.form["copies"]
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("books"))

    return render_template("add_book.html")

# ---------------- LOANS ----------------

@app.route("/issue/<int:book_id>")
@login_required
def issue(book_id):
    book = Book.query.get(book_id)

    if book.copies > 0:
        loan = Loan(user_id=current_user.id, book_id=book_id)
        book.copies -= 1
        db.session.add(loan)
        db.session.commit()

    return redirect(url_for("books"))

@app.route("/return/<int:loan_id>")
@login_required
def return_book(loan_id):
    loan = Loan.query.get(loan_id)

    if loan and not loan.return_date:
        loan.return_date = datetime.utcnow()
        book = Book.query.get(loan.book_id)
        book.copies += 1
        db.session.commit()

    return redirect(url_for("loans"))

@app.route("/loans")
@login_required
def loans():
    if current_user.role == "admin":
        loans = Loan.query.all()
    else:
        loans = Loan.query.filter_by(user_id=current_user.id).all()

    return render_template("loans.html", loans=loans)

@app.route("/overdue")
@login_required
def overdue():
    loans = Loan.query.filter(
        Loan.due_date < datetime.utcnow(),
        Loan.return_date == None
    ).all()

    return render_template("loans.html", loans=loans)

if __name__ == "__main__":
    # Use the port assigned by the server, or default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)