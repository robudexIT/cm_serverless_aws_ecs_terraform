from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database
from datetime import datetime

from utils.sanitize import sanitize_input
from cdr.agentcdr import get_call_summary
import utils.auth as auth
from utils.custom_exception import CustomError 
from typing import Optional



router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']


@router.get("/api/callsummaries/{callsummaries}")
def get_callsummaries(callsummaries: str, startdate: Optional[str] = None, 
                      enddate: Optional[str] = None, tagname: Optional[str] = None,
                      duration: Optional[str] = None, direction: Optional[str] = None,
                      verify = Depends(auth.verify_access_token)):
    agents_cdrs  = ""
    try:
      if verify:
        callsummaries = sanitize_input(callsummaries)
        match callsummaries:
            case "csdinbound":
                if all([startdate, enddate, tagname]):
                    startdate = sanitize_input(startdate)
                    enddate = sanitize_input(enddate)
                    tagname = sanitize_input(tagname)
                else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')
                     tagname = "all"  
                agents_cdrs = get_call_summary(startdate, enddate, "", "",tagname, "", "", callsummaries, f"{callsummaries}details", False, cursor)         
            case "csdoutbound" | "collection":
                 if all([startdate, enddate, tagname, duration, direction]):
                    startdate = sanitize_input(startdate)
                    enddate = sanitize_input(enddate)
                    tagname = sanitize_input(tagname)
                    duration  = sanitize_input(duration)
                    direction = sanitize_input(direction)     
                 else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')
                     tagname = "all"  
                     duration = "0"
                     direction = "UP"       
                 agents_cdrs = get_call_summary(startdate, enddate, "", "", tagname, duration, direction, callsummaries, f"{callsummaries}details", False,cursor)                                                         
                     
            case  "sales":
                pass
            
            case "missedcalls":
                if all(startdate, enddate):
                    startdate = sanitize_input(startdate)
                    enddate = sanitize_input(enddate)  
                else:
                     startdate = datetime.now().strftime('%Y-%m-%d')
                     enddate = datetime.now().strftime('%Y-%m-%d')       
                agents_cdrs = get_call_summary(startdate, enddate, "", "", "", "", "", callsummaries, f"{callsummaries}details", False, cursor)   
            case _:
                 raise CustomError("Invalid Parameters", http_status_code=403, details={"message": "Invalid Parameters"})  
             
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content= agents_cdrs,
                    
           )  
      else:
          raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})                                           
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
        
        



