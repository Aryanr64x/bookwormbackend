from fastapi import APIRouter, HTTPException, Depends 
from auth_utils import get_current_user
from dependecies import get_db
from sqlalchemy.orm import Session, selectinload
from schemas import CreateReview, ReviewsResponse
from models import Review, Book
from typing import List
reviewRouter = APIRouter(prefix = "/reviews", tags = ['reviews'])

@reviewRouter.post('/{book_id}')
def createReview(book_id: int,request: CreateReview ,user = Depends(get_current_user), db: Session = Depends(get_db)):
    
    # create a review
    review = Review(rating = request.rating, review_text = request.review_text, user_id = user.id, book_id = book_id)
    db.add(review)
    db.flush()
    
    # update avg_review and review_count in a book
    book = db.query(Book).filter(Book.id == book_id).first()
    avg = book.avg_review
    total = book.review_count
    sumTotal = avg * total
    newAvg = (sumTotal + request.rating) / (total + 1)
    book.avg_review = newAvg
    book.review_count = total + 1
    db.commit()
    db.refresh(review)

    return review



@reviewRouter.get('/{book_id}', response_model = List[ReviewsResponse])
def getReviews(book_id: int, user = Depends(get_current_user), db: Session = Depends(get_db)):
    reviews = db.query(Review).options(selectinload(Review.user)).filter(Review.book_id == book_id).all()

    return reviews



@reviewRouter.get('/hasReviewed/{book_id}')
def hasReviewed(book_id: int, user = Depends(get_current_user), db: Session = Depends(get_db)):
    review = db.query(Review).filter(user.id == Review.user_id, book_id == Review.book_id).first()
    if review == None:
        return {"hasReviewed": False}
    return {"hasReviewed": True}



