"""
This file has all the database queries
Author: Akshaya Revaskar
Date: 29-04-2020
"""

from ..config.create_db import DatabaseService
db = DatabaseService()
session = db.db_connection()


# query for saving the data
def save(result):
    if result:
        session.add(result)
        session.commit()
        session.close()
        return True
    else:
        return False


# query for getting data by id
def filter_by_user_id(table, user_id):
    result = session.query(table).filter_by(user_id=user_id).all()
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


# query for getting data by label name
def filter_by_name(table, name):
    result = session.query(table).filter_by(label_name=name).first()
    if result:
        return result
    else:
        return False


# query for getting data by id
def filter_by_note_and_user_id(table, id, user_id):
    result = session.query(table).filter_by(id=id, user_id=user_id).all()
    if result:
        return result
    else:
        return False


# query for getting data given email
def filter_by_email(table, email):
    result = session.query(table).filter_by(email=email).first()
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
def update_label(table, label_id, label_name):
    result = session.query(table).filter_by(id=label_id).first()
    if result:
        result.label_name = label_name
        session.commit()
        session.close()
        return True
    else:
        return False


# query for updating password given email and password
def update_note(table, id, **kwargs):

    result = session.query(table).filter_by(id=id).first()

    if kwargs.get('color') and kwargs.get('title') and kwargs.get('description'):
        color = kwargs.get('color')
        title = kwargs.get('title')
        description = kwargs.get('description')
        if result:
            result.color = color
            result.title = title
            result.description = description
            session.commit()
            session.close()
            return True
        else:
            return False

    elif kwargs.get('color') and kwargs.get('title'):
        color = kwargs.get('color')
        title = kwargs.get('title')
        if result:
            result.color = color
            result.title = title
            session.commit()
            session.close()
            return True
        else:
            return False

    elif kwargs.get('title') and kwargs.get('description'):
        title = kwargs.get('title')
        description = kwargs.get('description')
        if result:
            result.title = title
            result.description = description
            session.commit()
            session.close()
            return True
        else:
            return False

    elif kwargs.get('color') and kwargs.get('description'):
        color = kwargs.get('color')
        description = kwargs.get('description')
        if result:
            result.color = color
            result.description = description
            session.commit()
            session.close()
            return True
        else:
            return False

    elif kwargs.get('color'):
        color = kwargs.get('color')
        if result:
            result.color = color
            session.commit()
            session.close()
            return True
        else:
            return False

    elif kwargs.get('description'):
        description = kwargs.get('description')
        if result:
            result.description = description
            session.commit()
            session.close()
            return True
        else:
            return False

    elif kwargs.get('title'):
        title = kwargs.get('title')
        if result:
            result.title = title
            session.commit()
            session.close()
            return True
        else:
            return False


# method for updating trash note
def update_trash(table, id):
    result = session.query(table).filter_by(id=id).first()
    if result:
        result.is_trashed = 1
        session.commit()
        session.close()
        return True
    else:
        return False


# method for updating pin note
def update_pin(table, id, user_id):
    result = session.query(table).filter_by(id=id, user_id=user_id).first()
    if result:
        result.is_pinned = 1
        session.commit()
        session.close()
        return True
    else:
        return False


# method for updating archive note
def update_archive(table, id, user_id):
    result = session.query(table).filter_by(id=id, user_id=user_id).first()
    if result:
        result.is_archived = 1
        session.commit()
        session.close()
        return True
    else:
        return False


# method for restoring note
def update_restore(table, id, user_id):
    result = session.query(table).filter_by(id=id, user_id=user_id).first()
    if result:
        result.is_restored = 1
        result.is_trashed = 0
        session.commit()
        session.close()
        return True
    else:
        return False


# method for getting all the table data
def fetch_all(table):
    data = session.query(table).all()
    if data is not None:
        return data
    else:
        return None


# method for deleting record given id
def delete_record(table, id):
    result = session.query(table).filter_by(id=id).first()
    if result:
        session.delete(result)
        session.commit()
        return result
    else:
        return False

