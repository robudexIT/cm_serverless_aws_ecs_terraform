from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database

from utils.schemas import UserLogin
from utils.sanitize import sanitize_input
import utils.auth as auth

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']

router = APIRouter(tags=['Auth'])


@router.post("/api/login")
def user_login(user_credentials:UserLogin):
    try:
        extension = sanitize_input(user_credentials.extension) 
        secret = sanitize_input(user_credentials.secret)
        csd_agent = 0
        agentcalltype = ""
        collection_agent = 0
        blended = "0"
        
        cursor.execute("SELECT * FROM login WHERE extension=%s ", (user_credentials.extension,))

        user = cursor.fetchone()
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID CREDENTIALS")
        
        if user and user['secret'] == secret:
                cursor.execute("""SELECT * FROM calltype WHERE extension=%s""", (extension,))
                calltype = cursor.fetchone()
                
                cursor.execute("""SELECT COUNT(*) FROM csd_agents WHERE extension=%s""", (extension,))
                csd_agent = cursor.fetchone()
                
                cursor.execute("""SELECT COUNT(*) FROM collection_agents WHERE extension=%s""", (extension,))
                collection_agent = cursor.fetchone()
                
                if csd_agent['COUNT(*)'] == 1 and collection_agent['COUNT(*)'] == 1 :
                  blended = "1"
                
                if calltype :
                  agentcalltype = calltype['calltype']
                
                payload = {
                    'data': {
                        'extension': user['extension'],
                        'name': user['name'],
                        'position': user['position'],
                        'blended': blended,
                        'calltype': agentcalltype
                    }
                    
            
                }
                token = auth.create_access_token(payload)  
                print(token)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content= {'jwt': token, 'message': "Successful login" },
                    
                )
        else:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={'message': 'User Not exist or Invalid Passowrd'} 
                )    

    except Exception as e:
        return JSONResponse(
            content=f'Error: {str(e)}'
        )           
    
