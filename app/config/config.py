class Config():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:40101109@localhost:5432/database'      
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './static/img/'