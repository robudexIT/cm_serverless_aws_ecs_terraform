from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database



from cdr.agentcdr import get_search_number
import utils.auth as auth
from utils.sanitize import sanitize_input
from utils.custom_exception import CustomError


router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']



@router.get("/api/searchnumber/{search_type}")
def search_number( search_type: str, customer_number: str,verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if search_type not in ['customer','collectiondetails','csdinbounddetails', 'csdoutbounddetails']:
                raise CustomError("Invalid or missing parameters", http_status_code=403, details={"message": "Invalid or missing parameters"})
            customer_number = sanitize_input(customer_number)

            search_result = get_search_number(customer_number, search_type, cursor)
            
            return JSONResponse(
                status_code= status.HTTP_200_OK,
                content= search_result
            )
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 