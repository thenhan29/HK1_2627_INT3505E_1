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


# PUT /books/<id>
@app.put("/books/<int:book_id>")
def update_book(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({"error": "not found"}), 404

    data = request.get_json()

    if not data.get("title") or not data.get("author"):
        return jsonify({
            "error": "title and author required"
        }), 422

    book["title"] = data["title"]
    book["author"] = data["author"]

    return jsonify(book), 200


# PATCH /books/<id>
@app.patch("/books/<int:book_id>")
def patch_book(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({"error": "not found"}), 404

    data = request.get_json()

    if "title" in data:
        book["title"] = data["title"]

    if "author" in data:
        book["author"] = data["author"]

    return jsonify(book), 200


# DELETE /books/<id>
@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({"error": "not found"}), 404

    BOOKS.remove(book)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)