
from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database
import utils.auth as auth
import cdr.tag as tag
from utils.custom_exception import CustomError 
from utils.sanitize import sanitize_input

router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']


@router.get("/api/tags")
def get_all_tags(verify = Depends(auth.verify_access_token)):
   try:
       if verify:
           alltags = tag.select_all_tags(cursor)
           
           return JSONResponse(
               status_code= status.HTTP_200_OK,
               content= alltags
           )
       else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"}) 
       
   except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
        


@router.post("/api/tags/{tagtype}")
def create_tag(body:dict,tagtype:str,verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if tagtype not in ['collection', 'csdinbound', 'csdoutbound']:
                raise CustomError("Invalid Parameters", http_status_code=403, details={"message": "Invalid Parameters"})
            
            tagname = sanitize_input(body['tagname'])
            createdby = sanitize_input(body['createdby'])
            createddate = sanitize_input(body['createddate'])
            
            addtag = tag.create_tag(tagtype.upper(),tagname.upper(),createdby,createddate,cursor, connection)
            
            if addtag:
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content=addtag
                    
                )
            else:
                raise CustomError("Cannot Created Tag", http_status_code=403, details={"message": "Cannot Create Tag"}) 
            
        else:
              raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"}) 
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 

@router.delete("/api/tags")
def deletetag(body:dict,verify = Depends(auth.verify_access_token)):
    try:
        if verify:
           
            removetag = tag.delete_tag(body['tagId'],cursor,connection)
            if removetag:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=removetag
                )
            else:
                 raise CustomError("Cannot Delete Tag", http_status_code=403, details={"message": "Cannot Delete Tag"})     
        else:
             raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"}) 
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 