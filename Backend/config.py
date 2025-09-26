class Config:
    pass

class DevelopmentConfig(Config):
    JWT_EXPIRATION_DELTA = 432000 #5 days
    MEMORY_PUSHER_DELTA = 600 # 10 mins
    UPLOAD_FOLDER = "uploads"
    