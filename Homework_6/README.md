# Author-Book Management with SQLAlchemy

## Overview

This project simulates an author-book management system using SQLAlchemy, a popular Python SQL toolkit and Object-Relational Mapper (ORM). The project leverages Faker to generate mock data for authors and books, and demonstrates the implementation of a many-to-many relationship between authors and books in an SQLite database.

The system allows you to:
- Generate random authors and books.
- Query books with the most pages.
- Calculate the average number of pages across all books.
- Identify the youngest author.
- List authors without any books.
- Fetch authors with more than three books.

## Features

- **Many-to-Many Relationship**: Authors can write multiple books, and books can have multiple authors.
- **Faker for Mock Data**: Uses the `faker` library to generate realistic, fake data for authors and books.
- **SQLite Database**: Stores data in an SQLite database (`db.sqlite3`) with the SQLAlchemy ORM for database interaction.
- **SQLAlchemy ORM**: Cleanly models the relationships between authors and books.
- **Comprehensive Queries**: Includes several database queries, such as fetching books with the most pages, calculating average pages, and finding authors with no books.