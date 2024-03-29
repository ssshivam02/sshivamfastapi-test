from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
# from alembic import command,config
# from alembic.config import Config
# alembic_cfg = Config("./alembic.ini")



#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/testing_db"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

#@pytest.fixture(scope="module")
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) #this is will delete everything
    Base.metadata.create_all(bind=engine)  #---> this done by sqlalchemy
    #command.upgrade(alembic_cfg,"head")
    #command.downgrade(alembic_cfg,"base")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#@pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# fixture have scope
# default function
# we change it to module  fixture runs once in one module
# fixture scope default function, class, module, package, session
