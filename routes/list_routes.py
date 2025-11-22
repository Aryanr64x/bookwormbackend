from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from dependecies import get_db
from auth_utils import get_current_user
from schemas import ListRequest, ListResponse, AddBookToListRequest
from models import List, Book
from slugify import slugify


listRouter = APIRouter(prefix = "/lists", tags  = ["lists"])



@listRouter.get("")
def getLists(db:Session = Depends(get_db), auth_user = Depends(get_current_user)):
    lists = auth_user.lists
    return lists


@listRouter.post("", response_model = ListResponse)
def createList(request: ListRequest ,db:Session = Depends(get_db), auth_user = Depends(get_current_user)):
    new_list = List(name = request.name, slug = slugify(request.name), description = request.description, user_id = auth_user.id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list
                 



@listRouter.post("/add-book")
def addBook(request: AddBookToListRequest, db: Session = Depends(get_db), auth_user = Depends(get_current_user)):
    fetched_list = db.query(List).filter(List.id == request.list_id).first()
    if fetched_list == None: 
        raise HTTPException(status_code = 404, detail = "List Not Found")
    
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if book == None:
        raise HTTPException(status_code = 404, detail = "Book not found")
    

    if fetched_list not in book.lists:
        
        book.lists.append(fetched_list)
        db.commit()
        return {"message": "Successfully added book to list"}
    else:
        raise HTTPException(status_code = 400, detail = "Book already there in the list")
    


@listRouter.get('/{list_id}')
def getBooks(list_id: int,  db: Session = Depends(get_db)):
    fetch_list = db.query(List).options(selectinload(List.books)).filter(List.id == list_id).first()
    return fetch_list


