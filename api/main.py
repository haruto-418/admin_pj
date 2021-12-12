from fastapi import FastAPI


import firebase_admin
from firebase_admin import auth
from firebase_admin import firestore

from typing import Generator, List
import names
import random


from .common import functions
from .common import models
from .common import types

firebase_admin.initialize_app()

app: FastAPI = FastAPI()
db: firestore = firestore.client()


@app.post('/users/add')
async def create_random_user(how_many_users: int) -> None:
    """
    入力された整数分の名前・パスワード（6文字）は重複を考慮せずランダムに生成。
    メアドは重複した場合エラーメッセージを返しその処理を飛ばす。
    住所は東京都内の住所で重複を考慮せずランダムに生成。
    """
    for _ in range(how_many_users):
        email: str = functions.create_random_strings(False, 3)+'@sample.com'
        password: str = functions.create_random_strings(True, 6)
        name: str = names.get_first_name()
        address: str = functions.extract_from_file(
            '/src/api/assets/address_strings.csv')

        user: models.User = models.User(name, email, address)
        uid: str = user.create_account(password)
        try:
            db.collection('users').document(uid).set(
                {'name': name, 'email': email, 'address': address})
        except Exception as e:
            return {'firestore_error': e}


@ app.post('/users/delete')
async def delete_user(how_many_users: int) -> None:
    """
    指定した人数分、ユーザーを削除する。
    """
    user_ref: firestore.CollectionReference = db.collection('users')
    users: Generator = user_ref.stream()
    try:
        for _ in range(how_many_users):
            user: firestore.DocumentSnapshot = next(users)
            uid: str = user.id
            user_ref.document(uid).delete()
            models.User.delete_account(uid)
    except TypeError as e:
        return {'firestore_error': '登録ユーザーは0人です。{}'.format(e)}
    except Exception as e:
        return {'firestore_error': e}


@ app.post('/orders/add')
def add_order(how_many_orders: int) -> None:
    """
    ユーザーを取得して、ID等を読み取り、それに基づいたオーダーを追加する。
    """
    def fetch_user_from_firestore(how_many_users: int, doc_ref: firestore.CollectionReference, arr: List[str]) -> None:
        users: Generator = doc_ref.stream()
        for _ in range(how_many_users):
            user: firestore.DocumentSnapshot = next(users)
            user_data: dict = user.to_dict()
            arr.append([user.id, user_data['address']])

    user_ref: firestore.CollectionReference = db.collection('users')
    user_list: List[List[str]] = []

    fetch_user_from_firestore(how_many_orders, user_ref, user_list)

    try:
        order_strings: List[str] = []
        functions.read_file('/src/api/assets/order_strings.csv', order_strings)
        for i in range(how_many_orders):
            db.collection('orders').add({
                'createAt': firestore.SERVER_TIMESTAMP,
                'customerId': user_list[i][0],
                'deliveryAddress': user_list[i][1],
                'deliveryCharge': 0,
                'deliveryPoint': '',
                'maxQuotationPrice': 0,
                'minQuotationPrice': 0,
                'shopperId': '',
                'text': random.choice(order_strings)
            })
    except TypeError:
        return {'error': 'ユーザーが足りていません。'}
    except Exception as e:
        return {'error': e}
