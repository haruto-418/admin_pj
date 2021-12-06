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
    "千代田区九段南1-2-1",
    "中央区築地1-1-1",
    "港区芝公園1-5-25",
    "新宿区歌舞伎町1-4-1",
    "文京区春日1-16-21",
    "台東区東上野4-5-6",
    "墨田区吾妻橋1-23-20",
    "江東区東陽4-11-28",
    "品川区広町2-1-36",
    "目黒区上目黒2-19-15",
    "大田区蒲田5-13-14",
    "世田谷区世田谷4-21-27",
    "渋谷区宇田川町1-1",
    "中野区中野4-8-1",
    "杉並区阿佐谷南1-15-1",
    "豊島区南池袋2-45-1",
    "北区王子本町1-15-22",
    "荒川区荒川2-2-3",
    "板橋区板橋2-66-1",
    "練馬区豊玉北6-12-1",
    "足立区中央本町1-17-1",
    "葛飾区立石5-13-1",
    "江戸川区中央1-4-1",
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
