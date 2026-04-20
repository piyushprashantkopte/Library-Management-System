from app import app
from models import db, Book

def add_dummy_books():
    books = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, 5),
        ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, 3),
        ("1984", "George Orwell", "Dystopian", 1949, 8),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, 10),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy", 1997, 12),
        ("The Catcher in the Rye", "J.D. Salinger", "Classic", 1951, 4),
        ("Brave New World", "Aldous Huxley", "Dystopian", 1932, 6),
        ("The Alchemist", "Paulo Coelho", "Adventure", 1988, 15),
        ("Pride and Prejudice", "Jane Austen", "Romance", 1813, 7),
        ("The Da Vinci Code", "Dan Brown", "Thriller", 2003, 9),
        ("The Shining", "Stephen King", "Horror", 1977, 5),
        ("The Book Thief", "Markus Zusak", "Historical", 2005, 4),
        ("Dune", "Frank Herbert", "Sci-Fi", 1965, 11),
        ("Neuromancer", "William Gibson", "Cyberpunk", 1984, 3),
        ("The Martian", "Andy Weir", "Sci-Fi", 2011, 6),
        ("Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011, 10),
        ("Atomic Habits", "James Clear", "Self-Help", 2018, 20),
        ("Deep Work", "Cal Newport", "Productivity", 2016, 8),
        ("Foundation", "Isaac Asimov", "Sci-Fi", 1951, 5),
        ("The Little Prince", "Antoine de Saint-Exupéry", "Fable", 1943, 14)
    ]

    with app.app_context():
        for title, author, genre, year, copies in books:
            # Check if book already exists to avoid duplicates
            exists = Book.query.filter_by(title=title).first()
            if not exists:
                new_book = Book(
                    title=title, 
                    author=author, 
                    genre=genre, 
                    year=year, 
                    copies=copies
                )
                db.session.add(new_book)
        
        db.session.commit()
        print("Successfully added 20 dummy books!")

if __name__ == "__main__":
    add_dummy_books()