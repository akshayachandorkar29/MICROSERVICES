"""
This is the file for declaring all the tables and its fields
Author: Akshaya Revaskar
Date: 29-04-2020
"""
# importing necessary modules
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Column, Integer, String, Boolean


DeclarativeBase = declarative_base()


# defining Notes table with fields
class Notes(DeclarativeBase):
    """
    This is the class for creating Notes Model
    """
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    description = Column(String(100), nullable=True, default=None)
    color = Column(String(20), nullable=True, default=None)
    is_archived = Column(Boolean, nullable=False, default=False)
    is_trashed = Column(Boolean, nullable=False, default=False)
    is_restored = Column(Boolean, nullable=False, default=False)
    is_pinned = Column(Boolean, nullable=False, default=False)
    label_name = Column(String(50), nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    def __init__(self, title, **kwargs):
        self.title = title
        self.user_id = kwargs.get('user_id')
        self.description = kwargs.get('description')
        self.color = kwargs.get('color')
        self.is_archived = kwargs.get('is_archived')
        self.is_trashed = kwargs.get('is_trashed')
        self.is_restored = kwargs.get('is_restored')
        self.is_pinned = kwargs.get('is_pinned')
        self.label_name = kwargs.get('label_name')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')


# defining label table with fields
class Label(DeclarativeBase):
    """
    This is the class for creating Label model
    """
    __tablename__ = 'label'
    id = Column(Integer, primary_key=True)
    label_name = Column(String(250), nullable=False)

    def __init__(self, label_name):
        self.label_name = label_name
