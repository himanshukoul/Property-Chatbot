class Config:
    pass

class DevelopmentConfig(Config):
    SECRET_KEY = "helloworld"
    MONGO_URI = "mongodb://localhost:27017/"
    
    
"""from flask import Flask
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig) """