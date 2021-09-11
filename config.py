import os

class Config:
    DEBUG = False
    DEVELOPMENT = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.getenv(
        "SECRET_KEY", b"iJ\x9c\x11\xe3lE\x1a\xcf[\xc5\xf9\x8a\xab\\\x8b"
    )


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv(
        "SECRET_KEY", b"iJ\x9c\x11\xe3lE\x1a\xcf[\xc5\xf9\x8a\xab\\\x8b"
    )
