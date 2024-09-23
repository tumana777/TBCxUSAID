from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# SQLAlchemy setup
Base = declarative_base()

# Association table for many-to-many relationship between authors and books
author_book_association = Table(
    'author_book', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id', ondelete="CASCADE")),
    Column('book_id', Integer, ForeignKey('book.id', ondelete="CASCADE"))
)


# Define Author model
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    # Many-to-many relationship with Book through the association table
    books = relationship('Book', secondary=author_book_association, back_populates='authors')


# Define Book model
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    genre = Column(String)
    num_pages = Column(Integer)
    publish_year = Column(Integer)
    # Many-to-many relationship with Author through the association table
    authors = relationship('Author', secondary=author_book_association, back_populates='books')


# Create SQLite engine
engine = create_engine('sqlite:///db.sqlite3')

# Create tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()