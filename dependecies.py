from database import SessionLocal
from redis_client import redisClient
from fastapi import Request, HTTPException

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def rate_limit(request, limit = 30, window = 60):
    
    client_ip = request.client.host
    
    key = "rate_limit"+client_ip
    
    curr = redisClient.incr(1)
    
    if curr == 1:
        redisClient.expire(key, window)
    
    if curr > limit: 
            raise HTTPException(status_code = 402, detail = "Too much load on the server!!!")
        
        
