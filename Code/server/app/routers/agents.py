from fastapi import FastAPI, APIRouter, HTTPException, Response, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from config.database import Database


import utils.auth as auth
import utils.schemas as schemas
import agent.agent as agent
from utils.sanitize import sanitize_input
from utils.custom_exception import CustomError 
from config.database import Database


router = APIRouter()

db = Database()
connection_details = db.get_connection()
connection = connection_details['connection']
cursor = connection_details['cursor']


@router.get("/api/agents/csd/agentphonelogsdetails")
def get_csd_agentphonelogsdetails(extension: str,verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            extension = sanitize_input(extension)
            login_logout_details = agent.get_agent_inbound_login_logout_details(extension, cursor, connection)
            return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content= login_logout_details,
                            
            )                
            
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
@router.get("/api/agents/csd/inbound_group")
def get_csd_inbound_group(group: str,verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            group = sanitize_input(group)
            if group == 'active':
                can_receive_calls =1
                log = 'IN'
            elif group == 'inactive':
                can_receive_calls = 0
                log = 'OUT'
            else:
                raise CustomError("invalid or missing parameters", http_status_code=404, details={"message": "invalid invalid or missing parameters"})     
            active_inactive = agent.get_active_inactive_agents_in_inbound_group(can_receive_calls,log, cursor, connection)   
            
            return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content= active_inactive,
                            
                )  
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})    
           
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 

@router.get("/api/agents/{agent_type}/{extension}")
def get_agent(verify = Depends(auth.verify_access_token)):
    pass

@router.post("/api/agents/{agent_type}")
def create_agent(agentobj: schemas.CREATEANDUPDATEAGENT, agent_type: str, verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if agent_type is None or agent_type not in ['csd', 'collection']:
               raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})           
    
            name = sanitize_input(agentobj.name)
            email = sanitize_input(agentobj.email)
            extension = sanitize_input(agentobj.extension)
            
            create_agent= agent.create_agent(name, email, extension,agent_type,cursor, connection)
            
            if create_agent: 
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content=create_agent
                )
            
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 

@router.put("/api/agents/{agent_type}")
def update_agent(agentobj: schemas.CREATEANDUPDATEAGENT, agent_type: str,verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if agent_type is None or agent_type not in  ['csd', 'collection']:
              raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})   
            
            name = sanitize_input(agentobj.name)
            email = sanitize_input(agentobj.email)
            extension = sanitize_input(agentobj.extension)
            
            update_agent = agent.update_agent(name,email,extension,agent_type, cursor, connection) 
            
            if update_agent:
                return JSONResponse(
                    status_code= status.HTTP_201_CREATED,
                    content=update_agent
                )
            
                     
        else:
             raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 
@router.delete("/api/agents/{agent_type}/{extension}")
def delete_agent(extension: str, agent_type: str, verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if agent_type is None or agent_type not in ['csd', 'collection']:
                raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "}) 
            extension = sanitize_input(extension)
            delete_agent = agent.delete_agent(agent_type,extension, cursor, connection)
            
            if delete_agent:
                return JSONResponse(
                    status_code= status.HTTP_201_CREATED,
                    content=delete_agent
                )
            
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 

@router.get("/api/agents/{agent_type}")
def get_agents(agent_type: str, verify = Depends(auth.verify_access_token)):
    try:
        if verify:
            if agent_type is None or agent_type not in ['csd', 'collection']:
                 raise CustomError("Invalid or missing parameters ", http_status_code=404, details={"message": "Invalid or missing parameters "})
            
            agents =  agents = agent.get_agents(agent_type, cursor, connection)
            
            return JSONResponse(
                status_code= status.HTTP_200_OK,
                content= agents
            ) 
             
        else:
            raise CustomError("Not Authorize!! Token is Invalid", http_status_code=403, details={"message": "Not Authorize!! Token is Invalid"})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=f'Error: {str(e)}'
        ) 