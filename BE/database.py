from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# workbench에서 [tour_db] 데이터베이스 생성 후 사용
# create database tour_db;

DATABASE_URL = "mysql+pymysql://root:1234@localhost/tour_db"
# mysql+pymysql://[계정명]:[비밀번호]@[호스트주소]/[데이터베이스명]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()