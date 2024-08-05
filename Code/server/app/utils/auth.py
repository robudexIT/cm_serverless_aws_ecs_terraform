from jose import jwt, JWTError 
import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from utils.custom_exception import CustomError

from config.database import Database


# db = Database()
# connection_details = db.get_connection()
# connection = connection_details['connection']
# cursor = connection_details['cursor']


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Load environment variable from .env file
load_dotenv()

# import requests

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM =  os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])



def create_access_token(data : dict):
    try:
        
        to_encode = data.copy()
        
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({'exp': expire})
        
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encode_jwt
    except Exception :
        raise Exception({"message":"Cannot Create Token"})
    

def verify_access_token(token: dict = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        data = payload.get("data")
        
        if data['extension'] is None:
            return False
        else:
            return True
       

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail="Could not validate credentials",
                             headers={"WWW-Authenticate": "Bearer"} )
    
    
# def get_current_user(token: dict = Depends(oauth2_scheme), db= Depends(db)):
#     credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                              detail="Could not validate credentials",
#                              headers={"WWW-Authenticate": "Bearer"}               
#                              )  
#     user_id = verify_access_token(token, credentials_exceptions)
   
    
#     db['cursor'].execute("""SELECT  * FROM users WHERE id=%s""", (user_id,))
#     user = db['cursor'].fetchone()
    
#     if user is None:
#         raise credentials_exceptions 
    
#     return user        