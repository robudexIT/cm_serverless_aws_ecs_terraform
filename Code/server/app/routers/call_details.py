from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database
from datetime import datetime


import utils.auth as auth
from cdr.agentcdr import  get_call_agent_details
from utils.sanitize import sanitize_input
from config.database import Database
from utils.custom_exception import CustomError 


from typing import Optional



router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']




@router.get("/api/calldetails/{calldetails}")
def get_call_details(calldetails: str, startdate: Optional[str] = None, 
                      enddate: Optional[str] = None, tagname: Optional[str] = None,
                      duration: Optional[str] = None, direction: Optional[str] = None,
                      extension: Optional[str] = None, name: Optional[str] = None,
                      modalextension: Optional[str] = None , modalname: Optional[str] =None,
                      verify = Depends(auth.verify_access_token)):
    
    try:
        agents_cdrs_details = ""
        if verify:
            
            calldetails = sanitize_input(calldetails)
            match calldetails:
                case "csdinbounddetails":
                    calltype  = "csdinbound"
                    if all([extension,name, startdate, enddate, tagname]):
                        
                      extension = sanitize_input(extension)
                      username = sanitize_input(name)
                      startdate = sanitize_input(startdate)
                      enddate = sanitize_input(enddate)
                      tagname = sanitize_input(tagname)
                    elif all([modalextension, modalname, startdate, enddate,tagname]):
                      extension = sanitize_input(modalextension)
                      username = sanitize_input(modalname)
                      startdate = sanitize_input(startdate)
                      enddate = sanitize_input(enddate)
                      tagname = sanitize_input(tagname)     
                    else:
                       raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})                       
                    agents_cdrs_details = get_call_agent_details(extension, username, startdate, enddate, tagname, "", "", calltype, cursor)       
                case "csdoutbounddetails" | "collectiondetails":
                    to_remove = 'details'
                    calltype = calldetails.replace(to_remove, "") 
                    if all([extension,name, startdate, enddate, tagname,direction, duration]):
                      extension = sanitize_input(extension)
                      username = sanitize_input(name)
                      startdate = sanitize_input(startdate)
                      enddate = sanitize_input(enddate)
                      tagname = sanitize_input(tagname)  
                      direction = sanitize_input(direction)
                      duration = sanitize_input(duration)
                    elif all([modalextension, modalname, startdate, enddate,tagname,direction,duration]):
                      extension = sanitize_input(modalextension)
                      username = sanitize_input(modalname)
                      startdate = sanitize_input(startdate)
                      enddate = sanitize_input(enddate)
                      tagname = sanitize_input(tagname)  
                      direction = sanitize_input(direction)
                      duration = sanitize_input(duration)                                                
                    else:
                        raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."}) 
                    agents_cdrs_details = get_call_agent_details(extension, username, startdate, enddate, tagname, duration, direction, calltype,cursor)                   
                case "missedcallsdetails":
                    calltype = "missedcalls"
                    
                    if all([startdate, enddate]):
                      startdate = sanitize_input(startdate)
                      enddate = sanitize_input(enddate)                    
                      agents_cdrs_details = get_call_agent_details("", "", startdate, enddate, "", "", "", calltype,cursor)
                     
                    else: 
                        raise CustomError("query are missing, invalid or incomplete..", http_status_code=404, details={"message": "query are missing, invalid or incomplete.."})  
                case _:
                    raise CustomError("the details parameter are invalid..", http_status_code=404, details={"message": "the details parameter are invalid.."})                
            return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content= agents_cdrs_details,
                    
             )                 
                
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})    
   
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 