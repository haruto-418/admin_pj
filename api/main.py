import firebase_admin
from fastapi import FastAPI
from firebase_admin import auth
from firebase_admin import firestore

from typing import Generator, List
import names
import random

try:
    from common import functions
    from common import models
    from common import type_classes
except ModuleNotFoundError:
    from .common import functions
    from .common import models
    from .common import type_classes

if __name__ == 'api.main':
    app: FastAPI = FastAPI()
    firebase_admin.initialize_app()
    db: firestore = firestore.client()


@app.post('/users')
async def create_random_user(how_many_users: int) -> dict:
    """
    ユーザーを指定の人数作成する関数。
    """
    try:
        for _ in range(how_many_users):
            name: str = names.get_first_name()
            email: str = functions.create_random_strings(
                False, 3)+'@sample.com'
            address: str = functions.File.extract_from_file(
                '/src/api/assets/address_strings.csv')
            password: str = functions.create_random_strings(True, 6)

            user: models.User = models.User(name, email, address)
            user.create_account(password, db)

        return {'200': 'success!'}
    except Exception as e:
        return {'error': e}


@app.delete('/users')
async def delete_user(how_many_users: int) -> dict:
    """
    指定した人数分、ユーザーを削除する。
    """
    user_ref: firestore.CollectionReference = db.collection('users')
    try:
        for _ in range(how_many_users):
            models.User.delete_account(user_ref)
        return {'200': 'success!'}
    except TypeError as e:
        return {'firestore_error': 'There are no users.',
                'error': e}
    except Exception as e:
        return {'error': e}


@app.delete('/users/all')
async def delete_all_users() -> dict:
    """ユーザを全て削除する。"""
    try:
        id_arr: List[str] = functions.FirestoreFunc.get_all_document_id(
            db, 'users')
        functions.FirestoreFunc.delete_all(db, 'users')
        auth.delete_users(id_arr)
        return {'200': 'success!'}
    except Exception as e:
        return {'error': e}


@app.post('/orders')
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
        return {'200': 'success!'}

    except TypeError:
        return {'error': 'There are not enogh amount of users.'}
    except Exception as e:
        return {'error': e}
