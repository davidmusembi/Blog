import os


class Config:
    """
    General configuration parent class
    """
    SECRET_KEY = 'dave123'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    QUOTE_API_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'


class ProdConfig(Config):
    """
    Production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dave:toor@localhost:5432/blog'
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
}
