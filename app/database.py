from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  
#this is for pgadmin
from .config import settings
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine for creating local postgres connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

def get_db():
    '''
    create session: creating session locally
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
#for direct running raw sql
while True:
    try:
        #this hard code password and host name
        conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres',
        password='Shivam@1998',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error: ",error)
        time.sleep(2)
        #every two sec this will run again

'''