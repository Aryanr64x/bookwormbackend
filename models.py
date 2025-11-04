from database import Base
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique= True, index = True)
    password = Column(String , nullable=False)

    lists = relationship("List", back_populates = "user")



book_author = Table(
    "book_author",
    Base.metadata, 
    Column("book_id",Integer, ForeignKey("books.id"),primary_key = True),
    Column("author_id",Integer, ForeignKey("authors.id"),primary_key = True)
)


book_list = Table(
    "book_list",
    Base.metadata, 
    Column("book_id", Integer, ForeignKey("books.id"), primary_key  = True),
    Column("list_id", Integer, ForeignKey("lists.id"), primary_key = True)
)



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    slug = Column(String, nullable = False, index = True, unique = True)
   
    authors = relationship(
        "Author",
        secondary = "book_author",
        back_populates = "books"

    )


    lists = relationship(
        "List", 
        secondary = "book_list",
        back_populates = "books"
    )


    
    

class Author(Base):
    __tablename__  = "authors"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    slug = Column(String, nullable = False, index = True, unique = True)
    books = relationship(
        "Book",
        secondary = "book_author",
        back_populates = "authors"

    )



class List(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    slug = Column(String, nullable = False, index = True, unique = True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates = "lists")


    books = relationship("Book", secondary = "book_list", back_populates = "lists")

# create a list 
# add book to a list 