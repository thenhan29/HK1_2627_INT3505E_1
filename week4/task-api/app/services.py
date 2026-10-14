"""In-memory business logic for books, authors and borrow records.

Replace this module with a database-backed repository when required.
"""

BOOKS = {}
AUTHORS = {}
BORROWS = {}

_NEXT_BOOK_ID = 1
_NEXT_AUTHOR_ID = 1
_NEXT_BORROW_ID = 1

DEFAULT_BORROW_STATUS = "borrowed"


def _clean_text(value, default=""):
    """Strip strings; fall back to default when value is None or not a string."""
    if isinstance(value, str):
        return value.strip()
    return default


# ---------------------------------------------------------------------------
# Books
# ---------------------------------------------------------------------------

def _build_book(book_id, data):
    return {
        "id": book_id,
        "title": data["title"].strip(),
        "author": data["author"].strip(),
        "published_year": data["published_year"],
    }


def list_books():
    """Return all books ordered by ID."""
    return [BOOKS[key].copy() for key in sorted(BOOKS)]


def get_book(book_id):
    """Return a book or None when it does not exist."""
    book = BOOKS.get(book_id)
    return book.copy() if book else None


def create_book(data):
    """Create a book and assign its ID on the server."""
    global _NEXT_BOOK_ID

    book = _build_book(_NEXT_BOOK_ID, data)
    BOOKS[_NEXT_BOOK_ID] = book
    _NEXT_BOOK_ID += 1
    return book.copy()


def update_book(book_id, data):
    """Replace editable fields of an existing book."""
    if book_id not in BOOKS:
        return None

    BOOKS[book_id] = _build_book(book_id, data)
    return BOOKS[book_id].copy()


def delete_book(book_id):
    """Delete a book; return True if it existed."""
    return BOOKS.pop(book_id, None) is not None


# ---------------------------------------------------------------------------
# Authors
# ---------------------------------------------------------------------------

def _build_author(author_id, data):
    return {
        "id": author_id,
        "name": data["name"].strip(),
        "bio": _clean_text(data.get("bio"), default=""),
    }


def list_authors():
    """Return all authors ordered by ID."""
    return [AUTHORS[key].copy() for key in sorted(AUTHORS)]


def get_author(author_id):
    """Return an author or None when it does not exist."""
    author = AUTHORS.get(author_id)
    return author.copy() if author else None


def create_author(data):
    """Create an author and assign its ID on the server."""
    global _NEXT_AUTHOR_ID

    author = _build_author(_NEXT_AUTHOR_ID, data)
    AUTHORS[_NEXT_AUTHOR_ID] = author
    _NEXT_AUTHOR_ID += 1
    return author.copy()


def update_author(author_id, data):
    """Replace editable fields of an existing author."""
    if author_id not in AUTHORS:
        return None

    AUTHORS[author_id] = _build_author(author_id, data)
    return AUTHORS[author_id].copy()


def delete_author(author_id):
    """Delete an author; return True if it existed."""
    return AUTHORS.pop(author_id, None) is not None


# ---------------------------------------------------------------------------
# Borrows
# ---------------------------------------------------------------------------

def _build_borrow(borrow_id, data):
    status = _clean_text(data.get("status"), default="")
    return {
        "id": borrow_id,
        "book_id": data["book_id"],
        "borrower": data["borrower"].strip(),
        "status": status or DEFAULT_BORROW_STATUS,
        "borrow_date": data.get("borrow_date"),
    }


def list_borrows():
    """Return all borrow records ordered by ID."""
    return [BORROWS[key].copy() for key in sorted(BORROWS)]


def get_borrow(borrow_id):
    """Return a borrow record or None when it does not exist."""
    borrow = BORROWS.get(borrow_id)
    return borrow.copy() if borrow else None


def create_borrow(data):
    """Create a borrow record and assign its ID on the server."""
    global _NEXT_BORROW_ID

    borrow = _build_borrow(_NEXT_BORROW_ID, data)
    BORROWS[_NEXT_BORROW_ID] = borrow
    _NEXT_BORROW_ID += 1
    return borrow.copy()


def update_borrow(borrow_id, data):
    """Replace editable fields of an existing borrow record."""
    if borrow_id not in BORROWS:
        return None

    BORROWS[borrow_id] = _build_borrow(borrow_id, data)
    return BORROWS[borrow_id].copy()


def delete_borrow(borrow_id):
    """Delete a borrow record; return True if it existed."""
    return BORROWS.pop(borrow_id, None) is not None


# ---------------------------------------------------------------------------
# Reset helpers (tests only)
# ---------------------------------------------------------------------------

def reset_books():
    """Reset in-memory book state; intended for tests only."""
    global _NEXT_BOOK_ID
    BOOKS.clear()
    _NEXT_BOOK_ID = 1


def reset_authors():
    """Reset in-memory author state; intended for tests only."""
    global _NEXT_AUTHOR_ID
    AUTHORS.clear()
    _NEXT_AUTHOR_ID = 1


def reset_borrows():
    """Reset in-memory borrow state; intended for tests only."""
    global _NEXT_BORROW_ID
    BORROWS.clear()
    _NEXT_BORROW_ID = 1


def reset_all():
    """Reset every in-memory collection; intended for tests only."""
    reset_books()
    reset_authors()
    reset_borrows()