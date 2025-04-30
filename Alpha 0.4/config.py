class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/retoursdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'un-truc-ultra-secret-et-unique'