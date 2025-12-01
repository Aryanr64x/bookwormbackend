from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import text
from database import engine
from models import Book
from dependecies import get_db, rate_limit
from rapidfuzz import fuzz, process
import heapq

from sqlalchemy import func


bookRouter = APIRouter(prefix = "/books", tags = ['book'])


@bookRouter.get("/list/{last_id}")
def getBooks(last_id: int,db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.id > last_id).options(selectinload(Book.authors)).limit(12).all()
    return books



@bookRouter.get("/{slug}")
def getBooks(slug, db: Session = Depends(get_db)):
    book = db.query(Book).options(selectinload(Book.authors)).filter(Book.slug == slug).first()
    return book


@bookRouter.get('/search/titles')
def searchBook(q: str,request: Request,db:Session = Depends(get_db)):
    rate_limit(request, limit = 30, window = 60)
    if q.strip() == "":
        raise HTTPException(status_code=402, detail = "Must Provide a query string for this route")

    print(q)
    
    # Dont think like will slow down search as match will create a very small subset (search space) to search
    rows = db.execute(text(f"SELECT title from books_fts where title match '{q[0]}*' AND title LIKE '{q[0]}%'")).all()
    # fuzzy search 
    matches = process.extract(q, [r.title for r in rows], scorer = fuzz.WRatio, limit = 5)
    matched_titles = [match[0] for match in matches]
    print(matches)
    books = db.query(Book).filter(Book.title.in_(matched_titles)).all()
    # sort the books as per the matches 
    print([book.title for book in books])
    pq = []
    heapq.heapify(pq)
    imap = {}
    
    
    for i in range(len(matches)):
        imap[matches[i][0]] = i
    
    print(imap)    
    for book in books:
        heapq.heappush(pq, (imap[book.title], book))
    
    
    ordered_books = []
    while(len(pq) != 0):
        el = heapq.heappop(pq)
        print(el[1])
        ordered_books.append(el[1])
    
    print([book.title for book in ordered_books])
    
    return ordered_books
    
    
    
    
    




