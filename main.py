from fastapi import FastAPI,status,Depends
from typing import List
from create_db import engine,Base,SessionLocal
from sqlalchemy.orm import Session
import model
import schema

Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

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
