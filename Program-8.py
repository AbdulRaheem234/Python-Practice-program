from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "Python Crash Course", "author": "Eric Matthes"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"},
    {"id": 3, "title": "Clean Code", "author": "Robert Martin"}
]

# Helper function to find a book by ID


def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)

# GET all books


@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify({"books": books})

# GET single book


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book is None:
        abort(404, description="Book not found")
    return jsonify({"book": book})

# POST create a new book


@app.route('/api/books', methods=['POST'])
def create_book():
    if not request.json or 'title' not in request.json:
        abort(400, description="Title is required")

    # Generate new ID
    new_id = max(book['id'] for book in books) + 1 if books else 1

    book = {
        'id': new_id,
        'title': request.json['title'],
        'author': request.json.get('author', '')
    }

    books.append(book)
    return jsonify({"book": book}), 201

# PUT update an existing book


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if book is None:
        abort(404, description="Book not found")

    if not request.json:
        abort(400, description="No data provided")

    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])

    return jsonify({"book": book})

# DELETE a book


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book = find_book(book_id)
    if book is None:
        abort(404, description="Book not found")

    books = [book for book in books if book['id'] != book_id]
    return jsonify({"result": True}), 200

# Error handler


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400


if __name__ == '__main__':
    app.run(debug=True)
