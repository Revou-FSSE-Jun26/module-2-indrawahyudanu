import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:1234567@localhost:5432/revoshop_db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

