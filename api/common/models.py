import firebase_admin
from firebase_admin import auth
from firebase_admin import firestore
from google.cloud.firestore import Client


import geohash

try:
    from functions import FirestoreFunc
except ModuleNotFoundError:
    from .functions import FirestoreFunc


class User(object):
    def __init__(self, name: str, email: str, location: dict) -> None:
        self.name: str = name
        self.email: str = email
        self.location: dict = location

    def create_account(self, password: str, db: Client) -> None:
        """
        firebase_authenticationとfirestoreにユーザーを作成する関数。
        """
        try:
            user: auth.UserRecord = auth.create_user(
                email=self.email, password=password)
            db.collection('users').document(user.uid).set(
                {'name': self.name,
                 'email': self.email,
                 'address': self.location['address'],
                 'homeAddressPoint': {
                     'geohash': geohash.encode(float(self.location['latitude']), float(self.location['longtitude'])),
                     'geopoint': firestore.GeoPoint(float(self.location['latitude']), float(self.location['longtitude'])),
                 },
                 }
            )
        except Exception as e:
            return {"error": "fail to create user.", "error": e}

    @staticmethod
    def delete_account(coll_ref) -> None:
        try:
            user_id: List[str] = FirestoreFunc.get_document_id(coll_ref)
            coll_ref.document(user_id).delete()
            auth.delete_user(uid=user_id)
        except ValueError as e:
            return {'authentication_error': 'The uid is invalid.{}'.format(e)}
        except Exception as e:
            return {'authentication_error': 'fail to delete user.{}'.format(e)}
