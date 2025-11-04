from sqlalchemy.orm import Session
from models import Base
from database import engine, SessionLocal
from fastapi import FastAPI
from routes.auth_routes import authRouter
from routes.list_routes import listRouter
from routes.book_routes import bookRouter
from fastapi.middleware.cors import CORSMiddleware



# Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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


