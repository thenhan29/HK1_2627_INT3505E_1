from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

BOOKS = []
next_id = 1

DEFAULT_SIZE = 20
MAX_SIZE = 100


# GET /books
@app.get("/books")
def get_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify({
            "error": "page and size must be int"
        }), 400

    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    # Filter theo author
    filtered_books = BOOKS

    author = request.args.get("author")
    if author:
        filtered_books = [
            book for book in filtered_books
            if book["author"].lower() == author.lower()
        ]

    # Filter theo title
    q = request.args.get("q", "").lower()

    if q:
        filtered_books = [
            book for book in filtered_books
            if q in book["title"].lower()
        ]

    # Pagination
    total = len(filtered_books)
    start = (page - 1) * size
    end = start + size

    items = filtered_books[start:end]

    last_page = (total + size - 1) // size

    # HATEOAS links
    def url(p):
        return f"/books?page={p}&size={size}"

    links = {
        "self": {
            "href": url(page)
        },
        "first": {
            "href": url(1)
        },
        "last": {
            "href": url(max(last_page, 1))
        }
    }

    if page > 1:
        links["prev"] = {
            "href": url(page - 1)
        }

    if end < total:
        links["next"] = {
            "href": url(page + 1)
        }

    body = {
        "data": items,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": last_page
        },
        "_links": links
    }

    response = make_response(jsonify(body), 200)

    response.headers["Cache-Control"] = "public, max-age=30"

    return response


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
        return jsonify({
            "error": "not found"
        }), 404

    return jsonify(book)


# PUT /books/<id>
@app.put("/books/<int:book_id>")
def update_book(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({
            "error": "not found"
        }), 404

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
        return jsonify({
            "error": "not found"
        }), 404

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
        return jsonify({
            "error": "not found"
        }), 404

    BOOKS.remove(book)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)