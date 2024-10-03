import yookassa

from config import *
from constants import *

def create_payment(amount:int, description:str) -> tuple[str, int]:
    yookassa.Configuration.account_id = shopApi_id
    yookassa.Configuration.secret_key = shopApi_key

    payment = yookassa.Payment.create({
        "amount" : {
            "value" : amount,
            "currency" : "RUB"
        },
        "confirmation" : {
            "type" : "redirect",
            "return_url" : "https://t.me/royaty_request_bot"
        },
        "description" : description,
        "capture" : True
    })

    url = payment.confirmation.confirmation_url

    return url, payment.id

def check_payment(payment_id:int) -> bool:

    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return True

    return False
