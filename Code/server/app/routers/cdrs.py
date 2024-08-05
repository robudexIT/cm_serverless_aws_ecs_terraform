from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


import utils.auth as auth
from cdr.agentcdr import  get_single_cdr, update_single_cdr, insert_update_delete_customer
from utils.sanitize import sanitize_input
import utils.schemas as schemas
from utils.custom_exception import CustomError 
from config.database import Database
from typing import Optional

router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']

def custome_route(cdrtype, body, querytype, verify):
    try:
        if verify:
            if cdrtype is None or cdrtype not in  ['csdinbound','csdoutbound', 'collection', 'customer']:
               raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})  
           
            if cdrtype == 'customer':
                if querytype is None or querytype not in ['update', 'insert', 'delete']:
                    raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})
                customer_keys = ['customer_id', 'customer_name','customer_number', 'updated_by']
                if not None in [body.customer_id, body.customer_name, body.customer_number, body.updated_by]:
                    
            
                    customer_id = sanitize_input(body.customer_id)
                    customer_name = sanitize_input(body.customer_name)
                    customer_number = sanitize_input(body.customer_number)
                    updated_by = sanitize_input(body.updated_by)
                    
                    customer = insert_update_delete_customer(querytype, customer_id, customer_name, customer_number, updated_by,cursor,connection)   
                    
                    return customer
                            
                else:
                     raise CustomError("Invalid or missing body parameters ", http_status_code=404, details={"message": "Invalid or missing body parameters"}) 
            else:
                cdr_keys = ['whoansweredcall','caller', 'getdate','starttimestamp', 'comment', 'commentby', 'tag']
                if all(hasattr(body, key) for key in cdr_keys):
                     getdate =  sanitize_input(body.getdate) 
                     starttimestamp = sanitize_input(body.starttimestamp) 
                     extension = sanitize_input(body.whoansweredcall) 
                     comment = sanitize_input(body.comment)
                     commentby = sanitize_input(body.commentby)
                     tag = sanitize_input(body.tag)
                     update_cdr = update_single_cdr(cdrtype, extension, getdate, starttimestamp,comment,commentby,tag,cursor,connection)
                     
                     return update_cdr
                else:
                   raise CustomError("Invalid or missing body parameters ", http_status_code=404, details={"message": "Invalid or missing body parameters"})           
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    
    except Exception as e:
        raise Exception(e)
@router.put("/api/cdr/{cdrtype}")
def update(cdrtype: str,
               body: schemas.CUSTOMERANDCDRDATA,
               querytype: Optional[str] = None,
               verify = Depends(auth.verify_access_token)):
 
    try:
        result = custome_route(cdrtype, body, querytype, verify)    
        print(result)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
          
    
@router.post("/api/cdr/{cdrtype}")
def insert(cdrtype: str,
               body: schemas.CUSTOMERANDCDRDATA,
               querytype: Optional[str] = None,
               verify = Depends(auth.verify_access_token)):
    try:
        result = custome_route(cdrtype, body, querytype, verify)    
        print(result)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
          

@router.get("/api/cdr/{cdrtype}")
def get_cdr(cdrtype: str,  extension: Optional[str] = None,
            getdate: Optional[str] = None, starttimestamp: Optional[str] = None,
            verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if cdrtype is None or cdrtype not in  ['csdinbound','csdoutbound', 'collection', 'customer']:
               raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})  
           
            if cdrtype in ['csdinbound','csdoutbound', 'collection']:
                if all([extension, getdate,starttimestamp]):
                    extension = sanitize_input(extension) 
                    starttimestamp = sanitize_input(starttimestamp) 
                    getdate = sanitize_input(getdate) 
                    cdr = get_single_cdr(cdrtype,extension,getdate,starttimestamp,cursor) 
                    
                    return JSONResponse(
                        status_code= status.HTTP_200_OK,
                        content=cdr
                    )
                else:
                      raise CustomError("query parameter are missing, invalid or incomplete..", http_status_code=404, details={"message": "query paramters are missing, invalid or incomplete.."}) 
            else:
                 raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})        
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
        
@router.delete("/api/cdr/{cdrtype}")
def delete(cdrtype: str,
               body: schemas.CUSTOMERANDCDRDATA,
               querytype: Optional[str] = None,
               verify = Depends(auth.verify_access_token)):
 
    try:
        result = custome_route(cdrtype, body, querytype, verify)    
        print(result)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
          
