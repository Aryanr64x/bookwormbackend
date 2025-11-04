from dependecies import get_db
from schemas import SignUpRequest, SignUpResponse, AuthRequest
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt
from models import User 
import jwt
from datetime import datetime, timezone, timedelta
from auth_utils import get_current_user



authRouter = APIRouter(prefix = "/auth", tags = ['auth'])



def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))



@authRouter.get("/users")
def getusers(db:Session = Depends(get_db), auth_user = Depends(get_current_user)):
    print(auth_user.username)

    return db.query(User).all()


@authRouter.post("/signup", response_model = SignUpResponse)
def signup(request: SignUpRequest , db:Session = Depends(get_db)):
    print(request.username)
    user = db.query(User).filter(User.username == request.username).first()

    print(user)
    
    if user != None:
        raise HTTPException(status_code = 400, detail = "Usernames already taken")
    
    if request.password != request.password_repeat:
        raise HTTPException(status_code = 401, detail = "Password and Password Repeat should match ")
    
    new_user = User(username= request.username, password = get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    # jwt 
    payload = {
        "sub": str(new_user.id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    
    token = jwt.encode(payload, "SECRET", algorithm = "HS256")
    return {"user": new_user, "token": token}




@authRouter.post("/signin", response_model = SignUpResponse)
def signup(request: AuthRequest , db:Session = Depends(get_db)):
    print(request.username)
    user = db.query(User).filter(User.username == request.username).first()
        
    print(user)
    if user == None:
        raise HTTPException(status_code = 400, detail = "Username not found")
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code = 401, detail = "Incorrect Password ")
    
   


    # jwt 
    payload = {
        "sub": str(user.id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }


    token = jwt.encode(payload, "SECRET", algorithm = "HS256")
    return {"user": user, "token": token}