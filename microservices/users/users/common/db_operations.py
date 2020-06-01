"""
This file has all the database queries
Author: Akshaya Revaskar
Date: 29-04-2020
"""

from ..config.create_db import DatabaseService
db = DatabaseService()
session = db.db_connection()


def save(result):
    """
    method to save details in database
    :param result: object to be store
    :return: Boolean value
    """
    if result:
        session.add(result)
        session.commit()
        session.close()
        return True
    else:
        return False


def filter_by_email(table, email):
    """
    this is the method for retrieving data given email
    :param table: name of the table from which data to be retrieved
    :param email: email with which data to be retrieved
    :return: data or boolean value
    """
    result = session.query(table).filter_by(email=email).first()
    if result:
        return result
    else:
        return False


def filter_by_short(table, column_value):
    """
    this is the method for retrieving data given column_value
    :param table: name of the table from which data to be retrieved
    :param column_value: column_value with which data to be retrieved
    :return: data or boolean value
    """
    result = session.query(table).filter_by(short=column_value).first()
    if result:
        return result
    else:
        return False


def filter_by_id(table, id):
    """
    this is the method for retrieving data given id
    :param table: name of the table from which data to be retrieved
    :param id: id with which data to be retrieved
    :return: data or boolean value
    """
    result = session.query(table).filter_by(id=id).first()
    if result:
        return result
    else:
        return False


def update_password(table, id, new_password):
    """
    mehod for updating password
    :param table: table from which data to be retrieved
    :param id: id for which data to be retrieved
    :param new_password: new data to be entered
    :return: Boolean value
    """
    result = session.query(table).filter_by(id=id).first()
    if result:
        result.password = new_password
        session.commit()
        session.close()
        return True
    else:
        return False


def update_active(table, id):
    """
    method to update active flag
    :param table: table from which data to be retrived
    :param id: id for which data to be retrieved
    :return: Boolean value
    """
    result = session.query(table).filter_by(id=id).first()
    if result:
        result.active = 1
        session.commit()
        session.close()
        return True
    else:
        return False


# query for deleting query given id
def delete_query(table, id):
    """
    method to delete data from the data
    :param table: table from which data to be deleted
    :param id: id for which data to be deleted
    :return: data or boolean value
    """
    result = session.query(table).filter_by(id=id).first()
    if result:
        result.delete(synchronize_session=False)
        return result
    else:
        return False

