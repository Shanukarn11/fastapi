import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Depends
from routes.api import router as api_router
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()

origins = ["http://localhost:8000"]

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
@app.post('/token')
async def token(form_data: OAuth2PasswordRequestForm=Depends()):
    return {'access_token':form_data.username + 'token'}

@app.get('/testurl')
async def index(token : str = Depends(oauth2_scheme)):
    return {'the_token':token}



if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)
    print("running")
