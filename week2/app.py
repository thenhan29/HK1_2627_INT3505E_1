from flask import Flask, jsonify, request

app = Flask(__name__)

BOOKS = []
next_id = 1


# GET /books
@app.get("/books")
def get_books():
    return jsonify({
        "data": BOOKS,
        "total": len(BOOKS)
    })


# POST /books
@app.post("/books")
def create_book():
    global next_id

    data = request.get_json()

    if not data.get("title") or not data.get("author"):
        return jsonify({
            "error": "title and author required"
        }), 422

    book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"]
    }

    BOOKS.append(book)
    next_id += 1

    return jsonify(book), 201


# GET /books/<id>
@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({"error": "not found"}), 404

    return jsonify(book)


if __name__ == "__main__":
    app.run(debug=True)