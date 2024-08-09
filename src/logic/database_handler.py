import pymongo
import uuid
from logic.logging_handler import logger
import base64
import secrets

import pymongo
import uuid
import hashlib
from logic.date_handler import get_current_date


def generate_secure_token_base64(length=64):
    token_bytes = secrets.token_bytes(length)
    token_base64 = base64.urlsafe_b64encode(token_bytes).decode('utf-8')
    return token_base64


class Mongo:
    def __init__(self):
        self.dyn_server = ""
        self.dyn_db = ""
        self.user_collection = ""
        self.user = {
            "user_id": "",
            "username": "",
            "password_hash": "",
            "token": ""
        }

    # todo remove token

    def setup(self, server, db, user_collection):
        self.dyn_server = server
        self.dyn_db = db
        self.user_collection = user_collection

    def user_handling(self, username, password, register=False):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if register:
                username_document = dyn_collection.find_one({'username': username})
                if username_document:
                    return {"status": "ERROR", "message": "Username already taken"}
                user_id = str(uuid.uuid4())
                existing_document = dyn_collection.find_one({'user_id': user_id})
                if existing_document:
                    print(f"ERROR. Generated non unique ID. retrying...")
                    client.close()
                    return self.user_handling(username, password, register)
                new_user = {}
                for key, default_value in self.user.items():
                    new_user[key] = default_value

                new_user["user_id"] = user_id
                new_user["password_hash"] = password_hash
                new_user["username"] = username
                new_user["token"] = generate_secure_token_base64()
                dyn_collection.insert_one(new_user)
                client.close()
                return {"status": "OK", "user_id": user_id, "token": new_user["token"]}
            else:
                existing_document = dyn_collection.find_one({'username': username, 'password_hash': password_hash})
                if existing_document:
                    userid = existing_document["user_id"]
                    token = existing_document["token"]
                    client.close()
                    return {"status": "OK", "user_id": userid, "token": token}
                else:
                    print(f"User not found: {username}")
                    client.close()
                    return {"status": "ERROR", "message": "Username or password incorrect"}
        except Exception as e:
            print(e)
            return {"status": "ERROR", "message": "INTERNAL SERVER ERROR"}

    def get_data_with_list(self, user_id, items, collection):
        try:
            document = {}
            user_id = f"{user_id}"
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[collection]
            existing_document = dyn_collection.find_one({"user_id": user_id})
            if existing_document:
                for item in items:
                    document[item] = existing_document.get(item)
            else:
                print(f"No user found with userId: {user_id}")
                client.close()
                return None
            client.close()
            return document
        except Exception as e:
            print(e)
            return None

    def validate_token(self, token):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            existing_document = dyn_collection.find_one({"token": token})
            if existing_document:
                client.close()
                return {"status": "success", "message": "Token found", "user_id": existing_document["user_id"]}
            else:
                print(f"Token not found: {token}")
                client.close()
                return {"status": "error", "message": "Token not found"}
        except Exception as e:
            print(e)
            print(e)
            return {"status": "error", "message": "Internal Server Error"}

    def write_data_with_list(self, login, login_steam, items_dict):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            glob_id = ""
            if login_steam:
                steam_id = str(login)
                existing_document = dyn_collection.find_one({'steamid': steam_id})
                glob_id = steam_id
            else:
                user_id = str(login)
                existing_document = dyn_collection.find_one({"userId": user_id})
                glob_id = user_id
            if existing_document:
                update_query = {'$set': items_dict}
                if login_steam:
                    dyn_collection.update_one({'steamid': glob_id}, update_query)
                else:
                    dyn_collection.update_one({'userId': glob_id}, update_query)
                client.close()
                return {"status": "success", "message": "Data updated"}
            else:
                print(f"No user found with steamid: {glob_id}")
                client.close()
                return None
        except Exception as e:
            print(e)
            return None

    def add_to_array(self, userId, array_name, data):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            existing_document = dyn_collection.find_one({'userId': userId})
            if existing_document:
                update_query = {'$push': {array_name: data}}
                dyn_collection.update_one({'userId': userId}, update_query)
                client.close()
                return {"status": "success", "message": "Data updated"}
            else:
                print(f"No user found with userId: {userId}")
                client.close()
                return None
        except Exception as e:
            print(e)
            return None

    def update_array(self, userId, array_name, data, index):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            existing_document = dyn_collection.find_one({"userId": userId})
            if existing_document:
                update_query = {'$set': {f"{array_name}.{index}": data}}
                dyn_collection.update_one({'userId': userId}, update_query)
                client.close()
                return {"status": "success", "message": "Data updated"}
            else:
                print(f"No user found with userId: {userId}")
                client.close()
                return None
        except Exception as e:
            print(e)
            return None


mongo = Mongo()
