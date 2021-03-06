"""
This file contains database connection
Author: Akshaya Revaskar
Date: 29-04-2020
"""
# importing necessary modules
import warnings
import pymysql
pymysql.install_as_MySQLdb()
from ..models import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...settings import MYSQL_DB_CONFIG


class DatabaseService:
    """
    class for creating database connection and sesions
    """
    def db_connection(self):
        """
        this is the method for establishing database connection
        :return: session
        """
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                try:
                    db_engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'.format(**MYSQL_DB_CONFIG))
                    # db_engine.execute("CREATE DATABASE IF NOT EXISTS{}".format(MYSQL_DB_CONFIG.get("db_name")))
                    print("======> mysql database connected:{}".format(db_engine))
                    DeclarativeBase.metadata.create_all(db_engine)

                    if db_engine:
                        Session = sessionmaker()
                        Session.configure(bind=db_engine)
                        session = Session()
                    return session
                except ConnectionError:
                    raise Exception("Connection Error")
        except KeyError:
            print("Key Error")