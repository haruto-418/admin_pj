import firebase_admin
from firebase_admin import auth
from firebase_admin import firestore

try:
    from functions import FirestoreFunc
except ModuleNotFoundError:
    from .functions import FirestoreFunc


class User(object):
    def __init__(self, name: str, email: str, address: str) -> None:
        self.name: str = name
        self.email: str = email
        self.address: str = address

    def create_account(self, password: str, db_ref: firestore) -> None:
        """
        firebase_authenticationとfirestoreにユーザーを作成する関数。
        """
        try:
            user: auth.UserRecord = auth.create_user(
                email=self.email, password=password)
            db_ref.collection('users').document(user.uid).set(
                {'name': self.name, 'email': self.email, 'address': self.address}
            )
        except Exception as e:
            return {"error": "fail to create user.", "error": e}

    @staticmethod
    def delete_account(collection_ref) -> None:
        try:
            user_id = FirestoreFunc.get_document_id(collection_ref)
            collection_ref.document(user_id).delete()
            auth.delete_user(uid=user_id)
        except ValueError as e:
            return {'authentication_error': 'The uid is invalid.{}'.format(e)}
        except Exception as e:
            return {'authentication_error': 'fail to delete user.{}'.format(e)}
