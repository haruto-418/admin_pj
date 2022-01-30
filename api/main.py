import csv
import fastapi
import firebase_admin
import geohash

from fastapi import FastAPI
from firebase_admin import auth
from firebase_admin import firestore
from google.cloud.firestore import Client
from google.cloud.firestore import CollectionReference
from google.cloud.firestore import DocumentSnapshot


from typing import Generator
from typing import List
import names
import random

try:
    from common import functions
    from common import models
except ModuleNotFoundError:
    from .common import functions
    from .common import models


app: fastapi.applications.FastAPI = FastAPI()

firebase_admin.initialize_app()
db: Client = firestore.client()


@app.post('/v1/users')
async def create_random_user(how_many_users: int) -> dict[str, str]:
    """ユーザーを指定の人数作成する関数。"""
    with open('/src/api/assets/address_strings.csv', 'r')as f:
        reader: List[dict] = list(csv.DictReader(f))
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


@app.delete('/v1/users')
async def delete_user(how_many_users: int) -> dict[str, str]:
    """指定した人数分、ユーザーを削除する。"""
    user_coll_ref: CollectionReference = db.collection('users')
    try:
        for _ in range(how_many_users):
            models.User.delete_account(user_coll_ref)
        return {'200': 'success!'}
    except TypeError as e:
        return {'firestore_error': 'There are no users.',
                'error': e}
    except Exception as e:
        return {'error': e}


@app.delete('/v1/users/all')
async def delete_all_users() -> dict[str, str]:
    """ユーザを全て削除する。"""
    try:
        id_arr: List[str] = functions.FirestoreFunc.get_all_document_id(
            db, 'users')
        functions.FirestoreFunc.delete_all(db, 'users')
        auth.delete_users(id_arr)
        return {'200': 'success!'}
    except Exception as e:
        return {'error': e}


@app.post('/v1/orders')
async def add_order(how_many_orders: int) -> dict[str, str]:
    """オーダーを指定の個数作成する。"""
    users: Generator = db.collection('users').stream()
    order_strings: List[str] = []
    functions.File.read_file(
        '/src/api/assets/order_strings.csv', order_strings)
    try:
        for _ in range(how_many_orders):
            user_doc: DocumentSnapshot = next(users)
            user_dict: dict = user_doc.to_dict()
            db.collection('orders').add({
                'createAt': firestore.SERVER_TIMESTAMP,
                'userId': user_doc.id,
                'deliveryAddress': user_dict['address'],
                'deliveryCharge': 0,
                'deliveryPoint': {
                    'geohash': user_dict['homeAddressPoint']['geohash'],
                    'geopoint': user_dict['homeAddressPoint']['geopoint'],
                },
                'maxQuotationPrice': 0,
                'minQuotationPrice': 0,
                'workerId': '',
                'text': random.choice(order_strings)
            })
        return {'200': 'success!'}
    except TypeError:
        return {'error': 'There are not enough amount of users.'}
    except Exception as e:
        return {'error': e}


@app.delete('/v1/orders/all')
async def delete_all_orders() -> dict[str, str]:
    """オーダーを全て削除する。"""
    try:
        functions.FirestoreFunc.delete_all(db, 'orders')
        return {'200': 'success!'}
    except Exception as e:
        {'error': e}
