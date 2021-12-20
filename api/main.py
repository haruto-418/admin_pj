import csv
import firebase_admin
from fastapi import FastAPI
from firebase_admin import auth
from firebase_admin import firestore

from typing import Generator, List
import names
import random

import geohash

try:
    from common import functions
    from common import models
    from common import type_classes
except ModuleNotFoundError:
    from .common import functions
    from .common import models
    from .common import type_classes


app: FastAPI = FastAPI()
firebase_admin.initialize_app()
db: firestore = firestore.client()




@app.post('/users')
async def create_random_user(how_many_users: int) -> dict:
    """ユーザーを指定の人数作成する関数。"""
    with open('/src/api/assets/address_strings.csv', 'r')as f:
        reader: List = list(csv.DictReader(f))
    try:
        for _ in range(how_many_users):
            name: str = names.get_first_name()
            email: str = functions.create_random_strings(
                False, 3)+'@sample.com'
            location: dict = random.choice(reader)
            password: str = functions.create_random_strings(True, 6)

            user: models.User = models.User(name, email, location)
            user.create_account(password, db)

        return {'200': 'success!'}
    except Exception as e:
        return {'error': e}


@app.delete('/users')
async def delete_user(how_many_users: int) -> dict:
    """指定した人数分、ユーザーを削除する。"""
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
def add_order(how_many_orders: int) -> dict:
    """オーダーを指定の個数作成する。"""
    users = db.collection('users').stream()
    order_strings: List[str] = []
    with open('/src/api/assets/address_strings.csv', 'r')as f:
        reader = list(csv.DictReader(f))
    try:
        for _ in range(how_many_orders):
            user_doc = next(users)
            user_dict = user_doc.to_dict()
            db.collection('orders').add({
                'createAt': firestore.SERVER_TIMESTAMP,
                'customerId': user_doc.id,
                'deliveryAddress': user_dict['address'],
                'deliveryCharge': 0,
                'deliveryPoint': {
                    'geohash': '',
                    'geopoint': firestore.GeoPoint(1, 1)
                },
                'maxQuotationPrice': 0,
                'minQuotationPrice': 0,
                'shopperId': '',
                'text': random.choice(order_strings)
            })
            print('finish a roop')
        return {'200': 'success!'}
    except TypeError:
        return {'error': 'There are not enough amount of users.'}
    except Exception as e:
        return {'error': e}
