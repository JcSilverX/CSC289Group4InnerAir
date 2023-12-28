from decouple import config

DB_NAME = config('DB_NAME')
# HOST = config('HOST')
# USR = config('USR')
# PASSWD = config('PASSWD')


class Config(object):
    """
        profile pics
    """
    UPLOAD_FOLDER = config('UPLOAD_FOLDER')

    """
        base config.
    """
    SECRET_KEY = config('SECRET_KEY')
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT')
    DEBUG = False
    DEBUG_TB_ENABLED = False

    """
        MYSQL SETTINGS
    """
    # HOST = config('HOST')
    # USR = config('USR')
    # PASSWD = config('PASSWD')

    """
        mail settings.
    """
    MAIL_DEFAULT_SENDER = config('APP_MAIL_DEFAULT_SENDER')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = config('APP_MAIL_USERNAME')
    MAIL_PASSWORD = config('APP_MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    """""
        MySQL DB - SETUP
        'mysql+pymysql://username:password@localhost/DB_NAME' 
        
        You can replace <localhost> with the <URL> if you want to put it online.
        'mysql+pymysql://username:password@<url>/DB_NAME'
        
        NOTE:
            You can't use '-' to name the database. You would need to use '_' underscores.
            
            Example:
                instead of inner-air-dev would be inner_air_dev
    """""
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USR}:{PASSWD}@{HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
