from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    extension: str
    secret: str 



class CREATEANDUPDATEAGENT(BaseModel):
    name: str 
    email: EmailStr 
    extension: str
    
class CUSTOMERANDCDRDATA(BaseModel):
    customer_id:  Optional[str] = None
    customer_name:  Optional[str] = None
    customer_number: Optional[str] = None
    updated_by:  Optional[str] = None
    whoansweredcall:  Optional[str] = None
    caller:  Optional[str] = None
    starttimestamp:  Optional[str] = None 
    comment:  Optional[str] = None
    comment_by:  Optional[str] = None
    tag:  Optional[str] = None