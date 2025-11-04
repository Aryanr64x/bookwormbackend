from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from models import Book
from dependecies import get_db

bookRouter = APIRouter(prefix = "/books", tags = ['book'])


@bookRouter.get("")
def getBooks(db: Session = Depends(get_db)):
    books = db.query(Book).options(selectinload(Book.authors)).limit(10).all()
    return books 

@bookRouter.get("/{slug}")
def getBooks(slug,db: Session = Depends(get_db)):
    book = db.query(Book).options(selectinload(Book.authors)).filter(Book.slug == slug).first()
    return book


