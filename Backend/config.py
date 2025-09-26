class Config:
    pass

class DevelopmentConfig(Config):
    SECRET_KEY = "helloworld"
    #MONGO_URI = "mongodb://localhost:27017/"
    JWT_EXPIRATION_DELTA = 432000 #5 days
    MEMORY_PUSHER_DELTA = 600 # 10 mins
    UPLOAD_FOLDER = "uploads"
    