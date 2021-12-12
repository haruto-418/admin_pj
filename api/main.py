from fastapi import FastAPI
from fastapi import exceptions

import firebase_admin
from firebase_admin import auth
from firebase_admin import firestore

from typing import Generator, List
import names
import random
import string

from .common import functions

firebase_admin.initialize_app()

app: FastAPI = FastAPI()
db: firestore = firestore.client()

# TODO: (kikuchi) make tests of each functions.

# TODO: (kikuchi) rename the endpoits.

# TODO: (kikuchi) handle some errors.


@app.post('/users/add')
async def create_random_user(how_many_users: int) -> None:
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

        address_strings: List[str] = []

        functions.read_file(
            '/src/api/assets/address_strings.csv', address_strings)

        address: str = random.choice(address_strings)
        try:
            user: auth.UserRecord = auth.create_user(
                email=email, password=password)
            db.collection('users').add(
                {'name': name, 'email': email, 'address': address})
        except firebase_admin._auth_utils.EmailAlreadyExistsError:
            return {'error': '同じメールアドレスを持つユーザーが存在するため、処理を飛ばします。'}
        except Exception as e:
            return {'error': e}

# TODO: (kikuchi) rename the endpoits.
# TODO: (kikuchi) change the HTTP method.


@ app.post('/users/delete')
async def delete_user(how_many_users: int) -> None:
    """
    指定した人数分、ユーザーを削除する。
    """
    user_ref: firestore.CollectionReference = db.collection('users')
    users: Generator = user_ref.stream()
    try:
        for _ in range(how_many_users):
            user = next(users)
            user_ref.document(user.id).delete()
    except TypeError:
        return {'error': '登録ユーザーは0人です。'}
    except Exception as e:
        return {'error': e}

# TODO: (kikuchi) rename the endpoits.


@ app.post('/orders/add')
def add_order(how_many_orders: int):
    """
    ユーザーを取得して、ID等を読み取り、それに基づいたオーダーを追加する。
    """
    order_strings = []

    functions.read_file('/src/api/assets/order_strings.csv', order_strings)

    user_ref: firestore.CollectionReference = db.collection('users')
    users: Generator = user_ref.stream()

    user_list: List[List[str]] = []
    for _ in range(how_many_orders):
        user = next(users)
        user_data = user.to_dict()
        user_list.append([user.id, user_data['address']])

    try:
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


##################################

class User(object):
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

    def create_account(self):
        try:
            auth.create_user(email=self.email, password=self.password)
        except:
            return {"error": "ユーザー登録に失敗しました。"}

    def delete_account(self):
        pass
