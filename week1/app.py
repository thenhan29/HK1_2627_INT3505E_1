from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

STUDENTS = []

BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin"},
    {"id": 2, "title": "Pragmatic Programmer", "author": "D. Thomas"},
    {"id": 3, "title": "Python Basics", "author": "John Smith"},
]

next_book_id = 4


@app.route("/")
def index():
    return {"message": "Hello, API!"}


# Bài 2
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data}), 200


# Bài 3
@app.route("/students", methods=["POST"])
def create_student():
    body = request.get_json(silent=True) or {}

    name = body.get("name")

    if not name:
        return jsonify({"error": "name là bắt buộc"}), 400

    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa": body.get("gpa", 0.0)
    }

    STUDENTS.append(student)

    return jsonify(student), 201


# Bài 4 + Bài 6 - GET book theo ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)

    if book is None:
        return jsonify({"error": "not found"}), 404

    return jsonify(book), 200


# Bài 4 + Bài 6 - GET danh sách books
@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 20))
    q = request.args.get("q", "").strip().lower()

    items = [b for b in BOOKS if q in b["title"].lower()]

    return jsonify(items[:limit]), 200


# Bài 6 - POST tạo book
@app.route("/books", methods=["POST"])
def create_book():
    global next_book_id

    body = request.get_json(silent=True) or {}

    title = body.get("title")
    author = body.get("author")

    # 400 - thiếu title hoặc author
    if not title or not author:
        return jsonify({"error": "title+author required"}), 400

    book = {
        "id": next_book_id,
        "title": title,
        "author": author
    }

    BOOKS.append(book)
    next_book_id += 1

    # 201 - tạo thành công
    return jsonify(book), 201, {
        "Location": f"/books/{book['id']}"
    }


# Bài 6 - PUT + DELETE book
@app.route("/books/<int:book_id>", methods=["PUT", "DELETE"])
def modify_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)

    # 404 - không tìm thấy book
    if book is None:
        return jsonify({"error": "not found"}), 404

    # PUT - cập nhật book
    if request.method == "PUT":
        body = request.get_json(silent=True) or {}

        title = body.get("title")
        author = body.get("author")

        if title is not None:
            book["title"] = title

        if author is not None:
            book["author"] = author

        # 200 - update thành công
        return jsonify(book), 200

    # DELETE - xóa book
    BOOKS.remove(book)

    # 204 - xóa thành công, không có body
    return "", 204


# Bài 5 - HTTP Status Codes

ORDERS = {
    1: {"id": 1, "status": "pending"},
    2: {"id": 2, "status": "shipped"},
    3: {"id": 3, "status": "delivered"},
}


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = ORDERS.get(order_id)

    # 404 - không tìm thấy order
    if order is None:
        return jsonify({"error": "not found"}), 404

    # 409 - không thể xóa order đã shipped/delivered
    if order["status"] in ("shipped", "delivered"):
        return jsonify({"error": "cannot delete"}), 409

    # Xóa order
    ORDERS.pop(order_id)

    # 204 - xóa thành công, không có body
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)