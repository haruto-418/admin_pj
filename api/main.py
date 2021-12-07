from fastapi import FastAPI

import firebase_admin
from firebase_admin import auth, firestore

import names
import random
import string

firebase_admin.initialize_app()

app: FastAPI = FastAPI()
db: firestore = firestore.client()

address_arr: str = [
    ""
]

@app.post('/add/random')
def create_random_user(how_many_users: int) -> None:
    """
    入力された整数分の名前・パスワード（6文字）は重複を考慮せずランダムに生成。
    メアドは重複した場合エラーメッセージを返しその処理を飛ばす。
    住所は東京都内の住所で重複を考慮せずランダムに生成。
    """
    for _ in range(how_many_users):
        emailstr: str = ""
        email: str = emailstr.join(
            [random.choice(string.ascii_letters) for _ in range(3)])+"@sample.com"

        passwordstr: str = ""
        password: str = passwordstr.join(
            [random.choice(string.ascii_letters+string.digits) for _ in range(6)])

        name: str = names.get_first_name()

        with open('/src/api/assets/address_strings.csv','r')as f:
            address_strings=[]
            while True:
                line=f.readline()
                address_strings.append(line)
                if not line:
                    break
        address: str = random.choice(address_strings)

        try:
            user: auth.UserRecord = auth.create_user(
                email=email, password=password)
            db.collection('users').add(
                {'name': name, 'email': email, 'address': address})
        except firebase_admin._auth_utils.EmailAlreadyExistsError:
            return {'message': '同じメールアドレスを持つユーザーが存在するため、処理を飛ばします。'}
