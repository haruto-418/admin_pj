from firebase_admin import auth


class User(object):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

    def create_account(self,password):
        try:
            auth.create_user(email=self.email, password=password)
        except:
            return {"error": "ユーザー登録に失敗しました。"}

    def delete_account(self):
        pass
