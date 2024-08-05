from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database
from datetime import datetime

import utils.auth as auth
from utils.custom_exception import CustomError 
from utils.sanitize import sanitize_input


router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']


@router.get("/api/getcounts/{count}")
def get_counts(count: str, verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if count not in ['cdr', 'customer']:
                 raise CustomError("Invalid path parameter", http_status_code=403, details={"message": "Invalid path parameter"})
            if count == 'cdr':
                    data = []
                    getdate = datetime.now().strftime('%Y-%m-%d')
                    #get active agents
                    query = """SELECT COUNT(*) as active_agents FROM csd_agents WHERE receive_calls=1"""   
                    cursor.execute(query)
                    active_agents = cursor.fetchone()
                    
                    data.append({
                        'active_agents': active_agents['active_agents']
                    })
                  
                    # data.append({'active_agents': active_agents['active_agents']}) 
                    # return data
                    #get active agents
                    query = """SELECT COUNT(*) as inactive_agents FROM csd_agents WHERE receive_calls=0"""
                    cursor.execute(query)
                    inactive_agents = cursor.fetchone()
                    
                    data.append({'inactive_agents': inactive_agents['inactive_agents']})
                    
     
                
                    #summaries    
                    csdinboundsummaries = """SELECT COUNT(*) FROM csd_inbound_cdr WHERE getDate=%s"""
                    csdoutboundsummaries = """SELECT COUNT(*) FROM csd_outbound_cdr WHERE getDate=%s"""
                    collectionsummaries = """SELECT COUNT(*) FROM collection_outbound_cdr WHERE getDate=%s"""
                    salessummaries = """SELECT COUNT(*) FROM sales_outbound_cdr WHERE getDate=%s"""
                    missedcallssummaries = """SELECT COUNT(*) FROM csd_inbound_cdr WHERE getDate=%s AND CallStatus!='ANSWER'"""
                    
                    queries = [{'csdinboundsummaries': csdinboundsummaries}, {'csdoutboundsummaries': csdoutboundsummaries}, {'collectionsummaries': collectionsummaries}, {'missedcallssummaries': missedcallssummaries}]

                    for query in queries:
                        for key, value in query.items():  
                           cursor.execute(value,(getdate,))
                           counts = cursor.fetchone()
                           data.append({key: counts['COUNT(*)']})
                           
                    return JSONResponse(
                        status_code= status.HTTP_200_OK,
                        content=data
                    )       
            if count == 'customer':
                cursor.execute("""SELECT COUNT(*) AS customer_count FROM customer_info""")
                customer = cursor.fetchone()    
                
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=customer
                )        
                                        
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})  
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 




