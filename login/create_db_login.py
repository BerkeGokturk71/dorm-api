from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


#Create a sqlite engine instance
engineLogin =create_engine("sqlite:///dormlogin.db")

#Create declarative instance

BaseLogin = declarative_base()

#Create session local class from sessionmaker factory

SessionLocalLogin = sessionmaker(bind=engineLogin, expire_on_commit=False)
