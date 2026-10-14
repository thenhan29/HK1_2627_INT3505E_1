from flask import request


def _base_validation():
    if not request.is_json:
        return None, "Content-Type phải là application/json"

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, "Dữ liệu yêu cầu phải là một đối tượng JSON"
    return payload, None


def parse_book_payload(required_fields):
    payload, err = _base_validation()
    if err:
        return None, err

    missing = [field for field in required_fields if field not in payload]
    if missing:
        return None, f"Thiếu các trường bắt buộc: {', '.join(missing)}"

    title = payload.get("title")
    author = payload.get("author")
    year = payload.get("published_year")

    if "title" in required_fields and (
        not isinstance(title, str) or not title.strip()
    ):
        return None, "Trường 'title' phải là một chuỗi ký tự không được để trống"

    if "author" in required_fields and (
        not isinstance(author, str) or not author.strip()
    ):
        return None, "Trường 'author' phải là một chuỗi ký tự không được để trống"

    if "published_year" in required_fields:
        # Kiểu boolean trong Python là lớp con của int, cần loại bỏ tường minh
        if isinstance(year, bool) or not isinstance(year, int):
            return None, "Trường 'published_year' phải là một số nguyên"
        if year < 0:
            return None, "Trường 'published_year' phải lớn hơn hoặc bằng 0"

    return payload, None


def parse_author_payload(required_fields):
    payload, err = _base_validation()
    if err:
        return None, err

    missing = [field for field in required_fields if field not in payload]
    if missing:
        return None, f"Thiếu các trường bắt buộc: {', '.join(missing)}"

    name = payload.get("name")
    bio = payload.get("bio")

    if "name" in required_fields and (
        not isinstance(name, str) or not name.strip()
    ):
        return None, "Trường 'name' phải là một chuỗi ký tự không được để trống"

    if "bio" in payload and bio is not None:
        if not isinstance(bio, str):
            return None, "Trường 'bio' phải là một chuỗi ký tự"

    return payload, None


def parse_borrow_payload(required_fields):
    payload, err = _base_validation()
    if err:
        return None, err

    missing = [field for field in required_fields if field not in payload]
    if missing:
        return None, f"Thiếu các trường bắt buộc: {', '.join(missing)}"

    book_id = payload.get("book_id")
    borrower = payload.get("borrower")
    status = payload.get("status")

    if "book_id" in required_fields:
        if isinstance(book_id, bool) or not isinstance(book_id, int):
            return None, "Trường 'book_id' phải là một số nguyên"
        if book_id <= 0:
            return None, "Trường 'book_id' phải lớn hơn 0"

    if "borrower" in required_fields and (
        not isinstance(borrower, str) or not borrower.strip()
    ):
        return None, "Trường 'borrower' phải là một chuỗi ký tự không được để trống"

    if "status" in payload and status is not None:
        if not isinstance(status, str) or not status.strip():
            return None, "Trường 'status' phải là một chuỗi ký tự không được để trống"

    return payload, None