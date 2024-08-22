# test_config.py
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sanjay:password@localhost/taskDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
