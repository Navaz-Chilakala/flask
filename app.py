from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Mock database for users
users = {
    "admin": "secret"
}

# Mock database for books
books = [
    {'id': 1, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
    {'id': 2, 'title': '1984', 'author': 'George Orwell'}
]

@auth.verify_password
def verify_password(username, password):
    if username in users and 1:#users[username] == password:
        return username

@app.route('/books', methods=['GET'])
@auth.login_required
def get_books():
    return jsonify({'books': books})

@app.route('/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify(book)

@app.route('/books', methods=['POST'])
@auth.login_required
def create_book():
    new_book = request.get_json()
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    update_data = request.get_json()
    book.update(update_data)
    return jsonify(book)

@app.route('/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)












