import sqlite3

# Establish connection to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Fetch and print books that have the most pages
max_num_pages = cursor.execute("""
    SELECT books.id, books.title, books.genre, books.num_pages, books.publish_year, authors.first_name, authors.last_name
    FROM books
    JOIN authors  ON books.author_id = authors.id
    WHERE books.num_pages = (SELECT MAX(num_pages) FROM books)
""").fetchall()

print("Here are the books with the most pages:")

for row in max_num_pages:
    print({
        "Book_id": row[0],
        "Title": row[1],
        "Genre": row[2],
        "Num_pages": row[3],
        "Publish_year": row[4],
        "Author": f"{row[5]} {row[6]}"
    })

# Fetch and print all books pages average
print("\nAll the books pages average is", cursor.execute("SELECT AVG(books.num_pages) FROM books").fetchall()[0][0])

# Fetch and print youngest author
youngest_author = cursor.execute("SELECT * FROM authors WHERE birth_date = (SELECT MAX(birth_date) FROM authors)").fetchall()[0]
print(f"\nThe youngest author is '{youngest_author[1]} {youngest_author[2]}' born on '{youngest_author[3]}'")

# Fetch and print authors that has no books yet
authors_without_books = cursor.execute("""
    SELECT a.id, a.first_name, a.last_name FROM authors a
    LEFT JOIN books b ON a.id = b.author_id
    WHERE b.id IS NULL;
""").fetchall()

print("\nHere are the authors that has no books yet:")

for row in authors_without_books:
    print({
        "Author_id": row[0],
        "Name": row[1] + " " + row[2]
    })

# Get 5 authors, who has more than 3 books
authors_with_more3books = cursor.execute("""
    SELECT a.id, a.first_name, a.last_name, COUNT(b.id) AS book_count
    FROM authors a
    INNER JOIN books b ON a.id = b.author_id
    GROUP BY a.id, a.first_name, a.last_name
    HAVING COUNT(b.id) > 3
    LIMIT 5;

""")

print("\nHere are the 5 authors, who has more than 3 books:")

for row in authors_with_more3books:
    print({
        "Author_id": row[0],
        "Name": row[1] + " " + row[2],
        "Number_of_books": row[3]
    })