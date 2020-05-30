"""
This file has all the database queries
Author: Akshaya Revaskar
Date: 29-04-2020
"""

from ..config.create_db import DatabaseService
db = DatabaseService()
session = db.db_connection()


# query for saving data
def save(result):
    if result:
        session.add(result)
        session.commit()
        session.close()
        return True
    else:
        return False


# query for getting email by email
def filter_by_email(table, email):
    result = session.query(table).filter_by(email=email).first()
    if result:
        return result
    else:
        return False


def filter_data(table, column_name, column_value):
    result = session.query(table).filter_by(column_name=column_value).first()
    if result:
        return result
    else:
        return False


# query for getting data by specific field
def filter_by_short(table, column_value):
    result = session.query(table).filter_by(short=column_value).first()
    if result:
        return result
    else:
        return False


# query for getting data by id
def filter_by_id(table, id):
    result = session.query(table).filter_by(id=id).first()
    if result:
        return result
    else:
        return False


# getting boolean value when requesting the table data from id
def filter_by_all(self, table, id):
    if self.session.query(table).filter_by(id=id).all():
        return True
    else:
        return False


# query for updating password given email and password
def update_password(table, id,  new_password):
    result = session.query(table).filter_by(id=id).first()
    if result:
        result.password = new_password
        session.commit()
        session.close()
        return True
    else:
        return False


# query for updating active field when user clicks on the link
def update_active(table, id):
    result = session.query(table).filter_by(id=id).first()
    if result:
        result.active = 1
        session.commit()
        session.close()
        return True
    else:
        return False


# query for getting all the table data
def fetch_all(table):
    data = session.query(table).all()
    if data is not None:
        return data
    else:
        return None


# query for deleting record given id
def delete_record(table, id):
    result = session.query(table).filter_by(id=id).first()
    if result:
        session.delete(result)
        session.commit()
        return result
    else:
        return False


