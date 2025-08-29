class Config:
    pass

class DevelopmentConfig(Config):
    SECRET_KEY = "helloworld"
    MONGO_URI = "mongodb://localhost:27017/"
    JWT_EXPIRATION_DELTA = 432000 #5 days
    MEMORY_PUSHER_DELTA = 600 # 10 mins
    UPLOAD_FOLDER = "uploads"
    

"""from flask import Flask
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig) """