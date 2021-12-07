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


@app.post('/add')
def create_user(name: str, email: str, password: str, address: str) -> None:
    """
    手動で名前・住所・メアド・パスワード（6文字以上）を入力することで新規ユーザーを作成。
    メールアドレスが重複していた場合はエラーメッセージを返す。
    """
    try:
        user: auth.UserRecord = auth.create_user(
            email=email, password=password)
        db.collection('users').add(
            {'name': name, 'email': email, 'address': address})
    except firebase_admin._auth_utils.EmailAlreadyExistsError:
        return {'message': '同じメールアドレスを持つユーザーが既に存在しています'}


@app.post('/add/random')
def create_random_user(how_many_users: int) -> None:
    """
    入力された整数分の名前・パスワード（6文字）は重複を考慮せずランダムに生成。
    メアドは重複した場合エラーメッセージを返しその処理を飛ばす。
    住所は東京都内の住所で重複を考慮せずランダムに生成。
    """
    for _ in range(how_many_users):
        emailstr: str = ""
        passwordstr: str = ""
        email: str = emailstr.join(
            [random.choice(string.ascii_letters) for _ in range(3)])+"@sample.com"
        password: str = passwordstr.join(
            [random.choice(string.ascii_letters+string.digits) for _ in range(6)])
        name: str = names.get_first_name()
        address: str = random.choice(address_arr)
        try:
            user: auth.UserRecord = auth.create_user(
                email=email, password=password)
            db.collection('users').add(
                {'name': name, 'email': email, 'address': address})
        except firebase_admin._auth_utils.EmailAlreadyExistsError:
            return {'message': '同じメールアドレスを持つユーザーが存在するため、処理を飛ばします。'}
