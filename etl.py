import requests
import json
from database import engine, SessionLocal
from dependecies import get_db
from models import Base, Book, Author
from slugify import slugify

# Base.metadata.create_all(bind = engine)


def get_books():
    i = 1
    while(i < 500):
        url = f"https://openlibrary.org/search.json?subject=novel&language=eng&page={i}"
        res = requests.get(url)    

        if res.status_code != 200:
            print("Cannot fetch books")
            continue 
        
 
        books = res.json()['docs']

        try:
            with open('books.json', 'r') as f:
                old_books = json.load(f)
        except:
            old_books = []


        books.extend(old_books)
        print(len(books))
        print(i)
        print("-----------**********------------********-----------")
        with open('books.json', 'w') as f:
            json.dump(books, f)
        i+=1
    

    return "books fetched"
    


def populateTables():
    
    db = next(get_db())
    with open('books.json', 'r') as f:
        books = json.load(f)
  

    for book in books:
        print(book)
        print("---------------")
        authors = []
        for author_name in book.get('author_name', ['anonymous']):
            # query for the author
            
            author = db.query(Author).filter(Author.slug == slugify(author_name)).first()
            if author == None:
                author = Author(name = author_name, slug = slugify(author_name))
                db.add(author)
                db.flush()

        
            authors.append(author)
        db.commit()                

        # query for the book 
        querybook = db.query(Book).filter(Book.slug == slugify(book['title'])).first()
        if querybook == None:
            new_book = Book(title = book['title'],  slug = slugify(book['title']))
            new_book.authors = authors
            db.add(new_book)
            db.flush()
        db.commit()

populateTables()
# get_books()




