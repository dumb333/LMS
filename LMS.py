from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Mock data for the purposes of this example
books = {
    '1': {'title': '1984', 'author': 'George Orwell', 'available': True},
    '2': {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'available': True},
}

borrowings = {
    '1': {'userID': '101', 'bookID': '1', 'due_date': '2024-03-01'},
}

# Retrieve a list of all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Add a new book to the catalog
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book_id = str(max([int(k) for k in books.keys()]) + 1)
    books[book_id] = data
    return jsonify({book_id: data}), 201

# Retrieve details of a specific book by ID
@app.route('/books/<bookID>', methods=['GET'])
def get_book(bookID):
    book = books.get(bookID)
    if book is None:
        abort(404)
    return jsonify({bookID: book})

# Update details of a specific book by ID
@app.route('/books/<bookID>', methods=['PUT'])
def update_book(bookID):
    if bookID not in books:
        abort(404)
    data = request.get_json()
    books[bookID].update(data)
    return jsonify({bookID: books[bookID]})

# Remove a book from the catalog by ID
@app.route('/books/<bookID>', methods=['DELETE'])
def delete_book(bookID):
    if bookID not in books:
        abort(404)
    del books[bookID]
    return jsonify({'result': True})

# Retrieve a list of all current book borrowings
@app.route('/borrowings', methods=['GET'])
def get_borrowings():
    return jsonify(borrowings)

# Create a new borrowing record when a book is checked out
@app.route('/borrowings', methods=['POST'])
def add_borrowing():
    data = request.get_json()
    borrowing_id = str(max([int(k) for k in borrowings.keys()]) + 1)
    borrowings[borrowing_id] = data
    return jsonify({borrowing_id: data}), 201

# Retrieve details of a specific borrowing record by user ID and book ID
@app.route('/users/<userID>/borrowings/<bookID>', methods=['GET'])
def get_user_borrowing(userID, bookID):
    borrowing_record = {k: v for k, v in borrowings.items() if v['userID'] == userID and v['bookID'] == bookID}
    if not borrowing_record:
        abort(404)
    return jsonify(borrowing_record)

# Update a borrowing record (e.g., extend borrowing period)
@app.route('/users/<userID>/borrowings/<bookID>', methods=['PUT'])
def update_borrowing(userID, bookID):
    borrowing_record = next((item for item in borrowings.values() if item['userID'] == userID and item['bookID'] == bookID), None)
    if borrowing_record is None:
        abort(404)
    data = request.get_json()
    borrowing_record.update(data)
    return jsonify(borrowing_record)

# Delete a borrowing record when a book is returned
@app.route('/users/<userID>/borrowings/<bookID>', methods=['DELETE'])
def delete_borrowing(userID, bookID):
    borrowing_id = next((k for k, v in borrowings.items() if v['userID'] == userID and v['bookID'] == bookID), None)
    if borrowing_id is None:
        abort(404)
    del borrowings[borrowing_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
