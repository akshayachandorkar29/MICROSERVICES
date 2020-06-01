"""
This is the file for declaring all the tables and its fields
Author: Akshaya Revaskar
Date: 29-04-2020
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


DeclarativeBase = declarative_base()


class Users(DeclarativeBase):
    """
    this is the class for creating Users model
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    active = Column(Integer, nullable=False, default=0)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Short(DeclarativeBase):
    """
    this is the class for creating Short model
    """
    __tablename__ = 'short'
    id = Column(Integer, primary_key=True)
    short = Column(String(255), nullable=False)
    token = Column(String(250), nullable=False)

    def __init__(self, short, token):
        self.short = short
        self.token = token
