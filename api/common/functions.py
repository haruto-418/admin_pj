from firebase_admin import firestore
from google.cloud.firestore import Client
from google.cloud.firestore import CollectionReference
from google.cloud.firestore import DocumentSnapshot

from typing import Generator
from typing import List
from typing import Optional
import random
import string


class File(object):
    @staticmethod
    def read_file(path: str, arr: List[str]) -> None:
        with open(path, 'r')as f:
            while True:
                line: str = f.readline()
                if not line:
                    break
                arr.append(line)

    @staticmethod
    def extract_from_file(path: str) -> List[str]:
        arr: List = []
        File.read_file(path, arr)
        return random.choice(arr)


class FirestoreFunc(object):
    @staticmethod
    def get_collection_ref(db: Client, coll_name: str) -> CollectionReference:
        return db.collection(coll_name)

    @staticmethod
    def get_document_id(coll_ref: Optional[CollectionReference]) -> str:
        datas: Generator = coll_ref.stream()
        data: DocumentSnapshot = next(datas)
        return data.id

    @staticmethod
    def get_all_document_id(db: Client, coll_name: str) -> List[str]:
        id_arr: List[str] = []
        docs: Generator = db.collection(coll_name).stream()
        for doc in docs:
            id_arr.append(doc.id)
        return id_arr

    @staticmethod
    def delete_all(db: Client, coll_name: str) -> None:
        docs: Generator = db.collection(coll_name).stream()
        for doc in docs:
            doc.reference.delete()


def create_random_strings(is_digit: bool, characters: int) -> str:
    """
    ランダムな文字列を生成する関数。
    """
    if is_digit:
        return "".join([random.choice(string.ascii_letters+string.digits) for _ in range(characters)])
    else:
        return "".join([random.choice(string.ascii_letters) for _ in range(characters)])


if __name__ == '__main__':
    a = File.extract_from_file('/src/api/assets/order_strings.csv')
    print(a)
