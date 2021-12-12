from firebase_admin import auth


class User(object):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

    def create_account(self, password):
        """
        ユーザー登録し、uidを返す関数。
        """
        try:
            user = auth.create_user(email=self.email, password=password)
            return user.uid
        except:
            return {"error": "ユーザー登録に失敗しました。"}

    def delete_account(uid):
        try:
            auth.delete_user(uid=uid)
        except ValueError as e:
            return {'authentication_error': 'ユーザーIDが不正です。.{}'.format(e)}
        except Exception as e:
            return {'authentication_error': 'ユーザーの削除に失敗しました。{}'.format(e)}
