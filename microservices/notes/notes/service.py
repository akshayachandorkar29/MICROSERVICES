"""
This file has different note services
Author: Akshaya Revaskar
Date: 29-04-2020
"""
from nameko.rpc import rpc
from .common.db_operations import *
from .models import Notes, Label
from .config.redis_connection import RedisConnection
from .common.utils import *

redis = RedisConnection()


class NoteService(object):
    """
    This is the Note service class
    """
    name = 'noteService'

    # creating note service
    @rpc
    def create_note_service(self, request_data):
        """
        This method is for creating note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "Something went wrong!"
        }

        try:

            title = request_data.get('title')
            description = request_data.get('description')
            color = request_data.get('color')
            is_trashed = request_data.get('is_trashed')
            is_archived = request_data.get('is_archived')
            is_pinned = request_data.get('is_pinned')
            is_restored = request_data.get('is_restored')
            label_name = request_data.get('label_name')
            user_id = request_data.get('user_id')

            label = filter_by_name(Label, label_name)
            if label:
                if label.user_id == user_id:

                    # checking if coming data is not empty
                    if request_data is not None:
                        note = Notes(title=title,
                                     description=description,
                                     color=color,
                                     is_trashed=is_trashed,
                                     is_archived=is_archived,
                                     is_pinned=is_pinned,
                                     is_restored=is_restored,
                                     label_name=label_name,
                                     user_id=user_id
                                     )

                        # saving the note object
                        save(note)

                        response["success"] = True
                        response["message"] = "NOTE CREATED SUCCESSFULLY!"
                else:
                    response["message"] = "LABEL DOES NOT BELONG TO YOU"
            else:
                response["message"] = "LABEL DOES NOT EXIST..."

        except Exception:
            response = response

        return response

    # reading note service
    @rpc
    def read_note_service(self, request_data):
        """
        This method is for reading note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            user_id = request_data.get('user_id')

            # getting id from request
            if user_id is not None:
                # getting data from table
                notes = filter_by_user_id(table=Notes, user_id=user_id)

                if notes:

                    note_list = []
                    for note in notes:
                        note_dictionary = {"id": note.id, "title": note.title, "user_id": note.user_id,
                                           "description": note.description, "color": note.color,
                                           "is_archived": note.is_archived, "is_trashed": note.is_trashed,
                                           "is_restored": note.is_restored, "is_pinned": note.is_pinned,
                                           "label_name": note.label_name, "created_at": note.created_at,
                                           "updated_at": note.updated_at}

                        note_list.append(note_dictionary)

                    response["success"] = True
                    response["message"] = "NOTES READ SUCCESSFULLY!"
                    response["data"] = note_list

                else:
                    response["message"] = "USER DO NOT HAVE ANY NOTES!"

            else:
                response["message"] = "SOMETHING WENT WRONG!"

        except Exception:
            response = response

        return response

    # updating the note service
    @rpc
    def update_note_service(self, request_data):
        """
        This method is for updating note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            note_id = request_data.get('id')
            user_id = request_data.get('user_id')

            note = filter_by_id(table=Notes, id=note_id)
            if note:
                if note.user_id == user_id:

                    if request_data.get('color') and request_data.get('title') and request_data.get('description'):
                        color = request_data.get('color')
                        title = request_data.get('title')
                        description = request_data.get('description')

                        result = update_note(table=Notes, id=note_id, color=color, title=title, description=description)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"

                    if request_data.get('color') and request_data.get('title'):
                        color = request_data.get('color')
                        title = request_data.get('title')

                        result = update_note(table=Notes, id=note_id, color=color, title=title)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"

                    if request_data.get('color') and request_data.get('description'):
                        color = request_data.get('color')
                        description = request_data.get('description')

                        result = update_note(table=Notes, id=note_id, color=color, description=description)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"

                    if request_data.get('title') and request_data.get('description'):
                        title = request_data.get('title')
                        description = request_data.get('description')

                        result = update_note(table=Notes, id=note_id, title=title, description=description)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"

                    if request_data.get('title'):
                        title = request_data.get('title')

                        result = update_note(table=Notes, id=note_id, title=title)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"

                    if request_data.get('description'):
                        description = request_data.get('description')

                        result = update_note(table=Notes, id=note_id, description=description)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"

                    if request_data.get('color'):
                        color = request_data.get('color')

                        result = update_note(table=Notes, id=note_id, color=color)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE UPDATED SUCCESSFULLY"
                        else:
                            response["message"] = "ERROR In UPDATE!"
                else:
                    response["message"] = "NOTE DO NOT BELONG TO YOU..."
            else:
                response["message"] = "NOTE DOES NOT EXIST!"

        except Exception:
            response = response

        return response

    # delete note service
    @rpc
    def delete_note_service(self, request_data):
        """
        This method is for deleting note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')
            user_id = request_data.get('user_id')

            # getting data from table
            note = filter_by_id(table=Notes, id=note_id)

            if note:
                if note.user_id == user_id:

                    if note.is_trashed == 1:
                        result = delete_record(table=Notes, id=note_id)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE DELETED SUCCESSFULLY"
                    else:
                        result = update_trash(table=Notes, id=note_id)
                        if result:
                            response["success"] = True
                            response["message"] = "NOTE TRASHED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT BELONG TO YOU"

            else:
                response["message"] = "NOTE DOES NOT EXIST!"

        except Exception:
            response = response

        return response

    # pin note service
    @rpc
    def pin_note_service(self, request_data):
        """
        This method is for pin note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')
            user_id = request_data.get('user_id')

            # getting data from table
            note = filter_by_id(table=Notes, id=note_id)

            if note:
                if note.user_id == user_id:

                    result = update_pin(table=Notes, id=note_id, user_id=user_id)
                    if result:
                        response["success"] = True
                        response["message"] = "NOTE PINNED SUCCESSFULLY"
                    else:
                        response["message"] = "ERROR!!!"
                else:
                    response["message"] = "NOTE DOES NOT BELONG TO YOU"
            else:
                response["message"] = "NOTE DOES NOT EXIST"

        except Exception:
            response = response

        return response

    # pin note service
    @rpc
    def archive_note_service(self, request_data):
        """
        This method is for archiving note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')
            user_id = request_data.get('user_id')

            # getting data from table
            note = filter_by_id(table=Notes, id=note_id)

            if note:
                if note.user_id == user_id:
                    result = update_archive(table=Notes, id=note_id, user_id=user_id)
                    if result:
                        response["success"] = True
                        response["message"] = "NOTE ARCHIVED SUCCESSFULLY"
                    else:
                        response["message"] = "ERROR!!!"
                else:
                    response["message"] = "NOTE DOES NOT BELONG TO YOU"
            else:
                response["message"] = "NOTE DOES NOT EXIST"

        except Exception:
            response = response

        return response

    # pin note service
    @rpc
    def restore_note_service(self, request_data):
        """
        This method is for restoring note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')
            user_id = request_data.get('user_id')

            # getting data from table
            note = filter_by_id(table=Notes, id=note_id)

            if note:
                if note.user_id == user_id:
                    result = update_restore(table=Notes, id=note_id, user_id=user_id)
                    if result:
                        response["success"] = True
                        response["message"] = "NOTE RESTORED SUCCESSFULLY"
                    else:
                        response["message"] = "ERROR!!!"
                else:
                    response["message"] = "NOTE DOES NOT BELONG TO YOU"
            else:
                response["message"] = "NOTE DOES NOT EXIST"

        except Exception:
            response = response

        return response

    # service for listing all the notes
    @rpc
    def list_note_service(self, request_data):
        """
        This method is for listing note
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            notes = fetch_all(table=Notes)
            if notes:
                note_list = []
                for note in notes:

                    note_dictionary = {"id": note.id, "title": note.title, "user_id": note.user_id,
                                       "description": note.description, "color": note.color,
                                       "is_archived": note.is_archived, "is_trashed": note.is_trashed,
                                       "is_restored": note.is_restored, "is_pinned": note.is_pinned,
                                       "label_name": note.label_name, "created_at": note.created_at,
                                       "updated_at": note.updated_at}

                    note_list.append(note_dictionary)

                response["success"] = True
                response["message"] = "NOTES LISTED SUCCESSFULLY!"
                response["data"] = note_list

            else:
                response["message"] = "ERROR..."

        except Exception:
            response = response

        return response

    # service for creating label
    @rpc
    def create_label_service(self, request_data):
        """
        This method is for creating label
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            label_name = request_data.get('label_name')
            user_id = request_data.get('user_id')

            # checking request_data is there
            if label_name and user_id is not None:
                label = Label(label_name=label_name, user_id=user_id)

                # saving the label object
                save(label)
                response["success"] = True
                response["message"] = "Label Created Successfully!"

            else:
                response["message"] = "Some values are missing..."

        except Exception:
            response = response

        return response

    # service for reading label
    @rpc
    def read_label_service(self, request_data):
        """
        This method is for reading label
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """

        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            user_id = request_data.get('user_id')

            # getting id from request
            if user_id is not None:
                # getting data from table
                labels = filter_by_user_id(table=Label, user_id=user_id)

                if labels:
                    label_list = []
                    for label in labels:
                        label_dictionary = {"id": label.id, "user_id": label.user_id, "label_name": label.label_name}

                        label_list.append(label_dictionary)

                        response["success"] = True
                        response["message"] = "LABEL READ SUCCESSFULLY!"
                        response["data"] = label_list

                else:
                    response["message"] = "LABEL DOES NOT EXIST!"

            else:
                response["message"] = "something went wrong!"

        except Exception:
            response = response

        return response

    # services for updating label
    @rpc
    def update_label_service(self, request_data):
        """
        This method is for updating label
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            label_id = request_data.get('id')
            user_id = request_data.get('user_id')
            label_name = request_data.get('label_name')

            label = filter_by_id(Notes, label_id)
            if label:
                if label.user_id == user_id:
                    result = update_label(table=Label, label_id=label_id, label_name=label_name)

                    if result:
                        response["success"] = True
                        response["message"] = "LABEL UPDATED SUCCESSFULLY!"
                    else:
                        response["message"] = "ERROR..."
                else:
                    response["message"] = "LABEL DOES NOT BELONG TO YOU"
            else:
                response["message"] = "LABEL DOES NOT EXIST..."

        except Exception:
            response = response

        return response

    # service for deleting label
    @rpc
    def delete_label_service(self, request_data):
        """
        This method is for deleting label
        :param request_data: json data coming from user
        :return: response dictionary with message, data and success flag
        """

        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
            }
        try:
            # getting id from request_data
            label_id = request_data.get('id')
            user_id = request_data.get('user_id')

            label = filter_by_id(Notes, label_id)
            if label:
                if label.user_id == user_id:
                    # getting data from table
                    result = delete_record(table=Label, id=label_id)
                    if result:
                        response["success"] = True
                        response["message"] = "LABEL DELETED SUCCESSFULLY"
                    else:
                        response["message"] = "ERROR..."
                else:
                    response["message"] = "LABEL DOES NOT BELONG TO YOU"
            else:
                response["message"] = "LABEL DOES NOT EXIST..."

        except Exception:
            response = response

        return response
