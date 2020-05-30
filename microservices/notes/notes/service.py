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
    name = 'noteService'

    # creating note service
    @rpc
    def create_note_service(self, request_data):
        response = {
            "success": False,
            "message": "Something went wrong!"
        }

        try:

            # checking if coming data is not empty
            if request_data is not None:
                note = Notes(title=request_data.get('title'),
                             description=request_data.get('description'),
                             color=request_data.get('color'),
                             is_trashed=request_data.get('is_trashed'),
                             is_archived=request_data.get('is_archived'),
                             is_pinned=request_data.get('is_pinned'),
                             is_restored=request_data.get('is_restored'),
                             label_name=request_data.get('label_name'),
                             user_id=request_data.get('user_id')
                             )

                # saving the note object
                save(note)

                response["success"] = True
                response["message"] = "NOTE CREATED SUCCESSFULLY!"

        except Exception as e:
            print(e)

        return response

    # reading note service
    @rpc
    def read_note_service(self, request):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            note_id = request.get('id')

            # getting id from request
            if note_id is not None:
                # getting data from table
                note = filter_by_id(table=Notes, id=note_id)

                if note:
                    # converting coming data into json format
                    json_data = serialize_data(object=note)

                    response["success"] = True
                    response["message"] = "NOTE READ SUCCESSFULLY!"
                    response["data"] = json_data

                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            else:
                response["message"] = "something went wrong!"

        except Exception as e:
            print(e)

        return response

    # updating the note service
    @rpc
    def update_note_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            note_id = request_data.get('id')

            if request_data.get('color') and request_data.get('title') and request_data.get('description'):
                color = request_data.get('color')
                title = request_data.get('title')
                description = request_data.get('description')

                result = update_note(table=Notes, id=note_id, color=color, title=title, description=description)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            if request_data.get('color') and request_data.get('title'):
                color = request_data.get('color')
                title = request_data.get('title')

                result = update_note(table=Notes, id=note_id, color=color, title=title)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            if request_data.get('color') and request_data.get('description'):
                color = request_data.get('color')
                description = request_data.get('description')

                result = update_note(table=Notes, id=note_id, color=color, description=description)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            if request_data.get('title') and request_data.get('description'):
                title = request_data.get('title')
                description = request_data.get('description')

                result = update_note(table=Notes, id=note_id, title=title, description=description)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            if request_data.get('title'):
                title = request_data.get('title')

                result = update_note(table=Notes, id=note_id, title=title)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            if request_data.get('description'):
                description = request_data.get('description')

                result = update_note(table=Notes, id=note_id, description=description)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

            if request_data.get('color'):
                color = request_data.get('color')

                result = update_note(table=Notes, id=note_id, color=color)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE UPDATED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST!"

        except Exception as e:
            print(e)

        return response

    # delete note service
    @rpc
    def delete_note_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')

            if note_id is not None:
                # getting data from table
                note = filter_by_id(table=Notes, id=note_id)
                if note.is_trashed == 1:
                    result = delete_record(table=Notes, id=note_id)
                    if result:
                        response["success"] = True
                        response["message"] = "NOTE DELETED SUCCESSFULLY"
                    else:
                        response["message"] = "NOTE DOES NOT EXIST"
                else:
                    result = update_trash(table=Notes, id=note_id)
                    if result:
                        response["success"] = True
                        response["message"] = "NOTE TRASHED SUCCESSFULLY"
                    else:
                        response["message"] = "NOTE DOES NOT EXIST"
            else:
                response["message"] = "WRONG USER NOTE"

        except Exception as e:
            print(e)

        return response

    # pin note service
    @rpc
    def pin_note_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')

            if note_id is not None:
                result = update_pin(table=Notes, id=note_id)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE PINNED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST"
            else:
                response["message"] = "WRONG USER NOTE"

        except Exception as e:
            print(e)

        return response

    # pin note service
    @rpc
    def archive_note_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')

            if note_id is not None:
                result = update_archive(table=Notes, id=note_id)
                if result:
                    response["success"] = True
                    response["message"] = "NOTE ARCHIVED SUCCESSFULLY"
                else:
                    response["message"] = "NOTE DOES NOT EXIST"
            else:
                response["message"] = "WRONG USER NOTE"

        except Exception as e:
            print(e)

        return response

    # pin note service
    @rpc
    def restore_note_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # getting id from request_data
            note_id = request_data.get('id')

            if note_id is not None:
                # getting data from table
                note = filter_by_id(table=Notes, id=note_id)
                if note.is_trashed == 1:
                    result = update_restore(table=Notes, id=note_id)
                    if result:
                        response["success"] = True
                        response["message"] = "NOTE RESTORED SUCCESSFULLY"
                    else:
                        response["message"] = "NOTE DOES NOT EXIST"
                else:
                    response["message"] = "NOTE SHOULD BE TRASHED TO BE RESTORE"
            else:
                response["message"] = "WRONG USER NOTE"

        except Exception as e:
            print(e)

        return response

    # service for listing all the notes
    @rpc
    def list_note_service(self):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            notes = fetch_all(table=Notes)
            if notes:
                # converting data into json format
                json_data = serialize_data(notes)

                response["success"] = True
                response["message"] = "NOTES LISTED SUCCESSFULLY!"
                response["data"] = json_data

            else:
                response["message"] = "SOMETHING WENT WRONG..."

        except Exception as e:
            print(e)

        return response

    # service for creating label
    @rpc
    def create_label_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            label_name = request_data.get('label_name')

            # checking request_data is there
            if request_data is not None:
                label = Label(label_name=label_name)

                # saving the label object
                save(label)
                response["success"] = True
                response["message"] = "Label Created Successfully!"

            else:
                response["message"] = "Some values are missing..."

        except Exception as e:
            print(e)

        return response

    # service for reading label
    @rpc
    def read_label_service(self, request):

        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            label_id = request.get('id')

            # getting id from request
            if label_id is not None:
                # getting data from table
                label = filter_by_id(table=Label, id=label_id)

                if label:
                    # converting coming data into json format
                    json_data = serialize_data(object=label)

                    response["success"] = True
                    response["message"] = "LABEL READ SUCCESSFULLY!"
                    response["data"] = json_data

                else:
                    response["message"] = "LABEL DOES NOT EXIST!"

            else:
                response["message"] = "something went wrong!"

        except Exception as e:
            print(e)

        return response

    # services for updating label
    @rpc
    def update_label_service(self, request_data):
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            label_id = request_data.get('id')
            label_name = request_data.get('label_name')
            result = update_label(table=Label, id=label_id, label_name=label_name)

            if result:
                response["success"] = True
                response["message"] = "LABEL UPDATED SUCCESSFULLY!"
            else:
                response["message"] = "LABEl DOES NOT EXIST..."

        except Exception as e:
            print(e)

        return response

    # service for deleting label
    @rpc
    def delete_label_service(self, request_data):

        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
            }
        try:
            # getting id from request_data
            label_id = request_data.get('id')

            if label_id is not None:
                # getting data from table
                result = delete_record(table=Label, id=label_id)
                if result:
                    response["success"] = True
                    response["message"] = "LABEL DELETED SUCCESSFULLY"
                else:
                    response["message"] = "LABEL DOES NOT EXIST"

        except Exception as e:
            print(e)

        return response
