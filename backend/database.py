import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()

#devlopment
#db_url="postgresql://postgres:hello@localhost:5432/chatroom"

#deployment
db_url=os.getenv("DB_URL")


engine=create_engine(db_url)
session=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
