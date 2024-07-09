import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
load_dotenv()  # .env 파일에서 환경 변수 로드

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://username:password@localhost/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # 환경 변수에서 SECRET_KEY 로드, 없으면 무작위 값 사용
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': QueuePool,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800
    }