import firebase_admin
from firebase_admin import auth
from firebase_admin import firestore


class User(object):
    def __init__(self, name: str, email: str, address: str):
        self.name: str = name
        self.email: str = email
        self.address: str = address

    def create_account(self, password: str, db_ref: firestore):
        """
        firebase_authenticationとfirestoreにユーザーを作成する関数。
        """
        try:
            user: auth.UserRecord = auth.create_user(
                email=self.email, password=password)
            db_ref.collection('users').document(user.uid).set(
                {'name': self.name, 'email': self.email, 'address': self.address}
            )
            return user.uid
        except Exception as e:
            return {"error": "ユーザー登録に失敗しました。", "error": e}

    def delete_account(uid):
        try:
            auth.delete_user(uid=uid)
        except ValueError as e:
            return {'authentication_error': 'ユーザーIDが不正です。.{}'.format(e)}
        except Exception as e:
            return {'authentication_error': 'ユーザーの削除に失敗しました。{}'.format(e)}
