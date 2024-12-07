from fastapi import FastAPI,status,Depends
from typing import List
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from create_db import engine,Base,SessionLocal
from sqlalchemy.orm import Session
import model,schema
from middleware.log import RateLimitingMiddleware
#login file import
from login.create_db_login import BaseLogin,SessionLocalLogin,engineLogin
from login.model_login import Login
from login.schema_login import LoginSchema,SignUpSchema,Settings
from db_functions import get_password_hash,verify_password
#Base Login
BaseLogin.metadata.create_all(engineLogin)
print("user tablosu oluşturuldu")
Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(RateLimitingMiddleware)

@AuthJWT.load_config
def get_config():
    return Settings()
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
def get_login_session():
    sessionLogin = SessionLocalLogin()
    try:
        yield sessionLogin
    finally:
        sessionLogin.close()
@app.post("/sign", status_code=status.HTTP_201_CREATED)
async def sign(sign:SignUpSchema, session:Session = Depends(get_login_session)):
    db_user = session.query(Login).filter(Login.username == sign.username).first()
    if db_user is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user name already exists")

    new_user = Login(
        username=sign.username,
        password=get_password_hash(sign.password),
    )
    session.add(new_user)
    session.commit()
    return new_user


@app.post("/login", status_code=200)
async def login(user:LoginSchema,session:Session = Depends(get_login_session),Authorize:AuthJWT=Depends()):
    db_user = session.query(Login).filter(Login.username == user.username).first()
    if db_user and verify_password(db_user.password,user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        response = {
            "username": access_token,
            "password":user.username
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid username or password")

@app.get("/tasks/{date}/{meal_type}", response_model=List[schema.Task])
def read_task(date: str, meal_type: str ,session:Session=Depends(get_session)):
    todo_list = session.query(model.ToDo).filter(model.ToDo.date == date,model.ToDo.task== meal_type).all()
    return todo_list

@app.post("/tasks/",response_model=schema.Task,status_code=status.HTTP_201_CREATED)
def create_task(task:schema.ToDoCreate,session:Session = Depends(get_session)):
    tododb = model.ToDo(**task.dict())

    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    return tododb


