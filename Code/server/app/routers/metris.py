from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from datetime import datetime

from cdr.agentcdr import get_call_summary,  get_metrics_based_on_tag
from utils.sanitize import sanitize_input
from utils.custom_exception import CustomError 
import utils.auth as auth
from config.database import Database
from typing import Optional

router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']

@router.get("/api/getmetrics")
def get_metrics( start_date_and_time: Optional[str] = None, 
                      end_date_and_time: Optional[str] = None, option_metrics: Optional[str] = None,
                      duration_weight: Optional[str] = None, callcount_weight: Optional[str] = None,
                      group: Optional[str] = None,
                      verify = Depends(auth.verify_access_token)):
    try:
        generate_metrics = []
        if verify:
            
            if all([group, start_date_and_time,end_date_and_time,duration_weight,callcount_weight,option_metrics]):
                start_date_and_time = sanitize_input(start_date_and_time)
                end_date_and_time = sanitize_input(end_date_and_time)
                calltype = sanitize_input(group)
                option_metrics = sanitize_input(option_metrics)
                duration_weight = sanitize_input(duration_weight)
                callcount_weight = sanitize_input(callcount_weight)
                transform_start_date_and_time = start_date_and_time.strip().replace(":", "").replace("-", "").replace(" ", "-")
                transfrom_end_date_and_time =  end_date_and_time.strip().replace(":", "").replace("-", "").replace(" ", "-")            
                if option_metrics == 'tag':
                    generate_metrics = get_metrics_based_on_tag(transform_start_date_and_time, transfrom_end_date_and_time, calltype,cursor)                   

                else:
                    generate_metrics = get_call_summary("", "", transform_start_date_and_time , transfrom_end_date_and_time, "all", "", "", calltype, "", True,cursor)
                    generate_metrics[1]['duration_weight'] = duration_weight
                    generate_metrics[1]['callcount_weight'] = callcount_weight
                    generate_metrics[1]['datetimeRange'] = f"{start_date_and_time}  To {end_date_and_time}"
                    
                
                return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content= generate_metrics,
                            
                )    
            else:
                raise CustomError("There are missing query", http_status_code=404, details={"message": "There are missing query"})    
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})     
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 