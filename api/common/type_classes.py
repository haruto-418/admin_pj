from firebase_admin import firestore

from typing import Any
from typing import TypedDict


class Order(TypedDict):
    createAt: Any
    customerId: str
    deliveryAddress: str
    deliveryCharge: int
    deliveryPoint: Any
    maxQuotationPrice: int
    minQuotationPrice: int
    shopperId: str
    text: str
