from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import login, call_summary, call_details, metris,agents,cdrs, search_number, counts, tag


app = FastAPI()

@app.get("/status")
def check_getstaus():
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"message": "I am up.."}
                    
    )
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(login.router)
app.include_router(call_summary.router)
app.include_router(call_details.router)
app.include_router(metris.router)
app.include_router(agents.router)
app.include_router(cdrs.router)
app.include_router(search_number.router)
app.include_router(counts.router)
app.include_router(tag.router)