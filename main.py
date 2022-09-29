
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Depends,HTTPException, status
from routes.api import router as api_router
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from models.models import Base,Users
from db.database import Database
from models.request import User
from models.response import Response
from sqlalchemy import and_, desc


from datetime import datetime, timedelta
from typing import Union


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


database = Database()
engine = database.get_db_connection()
Base.metadata.create_all(engine)

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


pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@app.post('/user')
async def create_user(request:User):
    new_user = Users()
    new_user.PrimaryContactEmailAddress = request.PrimaryContactEmailAddress
    new_user.FirstName = request.FirstName
    new_user.LastName = request.LastName
    new_user.Password = get_password_hash(request.Password)
    new_user.PrimaryContactPhoneNumber = request.PrimaryContactPhoneNumber
    new_user.Status = request.Status
    new_user.Type = request.Type
   
    session = database.get_db_session(engine)
    session.add(new_user)
    session.flush()
    # get id of the inserted product
    session.refresh(new_user, attribute_names=['PrimaryContactEmailAddress'])
    data = {"PrimaryContactEmailAddress": new_user.PrimaryContactEmailAddress,"Password":new_user.Password }
    session.commit()
    session.close()
    return Response(data, 200, "Product added successfully.", False)
  
@app.get("/user/{email}")
async def read_product(email: str):
    session = database.get_db_session(engine)
    response_message = "Product retrieved successfully"
    data = None
    try:
        data = session.query(Users).filter(
            and_(Users.PrimaryContactEmailAddress == email)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Product Not found"
    error = False
    return Response(data, 200, response_message, error)
if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)
    print("running")


