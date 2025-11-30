from sqlalchemy.orm import Session
from models import Base
from database import engine, SessionLocal
from fastapi import FastAPI
from routes.auth_routes import authRouter
from routes.list_routes import listRouter
from routes.book_routes import bookRouter
from routes.review_routes import reviewRouter
from fastapi.middleware.cors import CORSMiddleware


# below line of code was commented because of alembic
# Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://bookwormfrontend.vercel.app"
]



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],   
    allow_headers = ["*"]         
)

app.include_router(authRouter)
app.include_router(bookRouter)
app.include_router(listRouter)
app.include_router(reviewRouter)

