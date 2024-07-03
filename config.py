import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.db_name = os.environ.get('DATABASE_NAME')
        self.db_type = os.environ.get('DB_TYPE')
        self.db_host = os.environ.get('HOST_ADDRESS')
        self.db_port = os.environ.get('PORT')
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')


    def get_dsn(self):
        return f'{self.db_type}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
