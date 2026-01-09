import uuid
from random import randint
from dotenv import load_dotenv
import os

from pprint import pprint

from paynow_sdk import CartItem, Payment, PaymentMethod, Paynow, PaynowConfig, TestMode

load_dotenv()

# your server endpoints to handle redirects and results
redirect_on_success_callback_url = "http://localhost:8000/paynow/redirect"
transaction_update_callback_url  = "http://localhost:8000/paynow/status"

zwg_config = PaynowConfig(
    os.getenv('ZWG_INTEGRATION_ID'),
    os.getenv('ZWG_INTEGRATION_KEY'),
    "ZWG"
)

usd_config = PaynowConfig(
    os.getenv('USD_INTEGRATION_ID'),
    os.getenv('USD_INTEGRATION_KEY'),
    "USD"
)

api = Paynow(
    config=[zwg_config, usd_config], 
    redirect_callback_url=redirect_on_success_callback_url, 
    status_callback_url=transaction_update_callback_url
)

amount = 1.50
currency="USD"
ref = str(uuid.uuid4())
trace = "txn-trace-" + str(randint(1000, 9999))

def poll(url):
    print("============== POLLING ================\n")
    poll_response = api.poll_url(url)
    pprint(poll_response)

def trace_txn(txn_trace):
    print("============== TRACE TXN ================\n")
    trace_response = api.trace_transaction(txn_trace, currency)
    pprint(trace_response)


def test():
    print(f'Initiating payment with Ref: {ref} | Trace: {trace} | Amount: {amount}\n')

    payment = Payment(
        merchant_reference=ref,
        merchant_trace=trace,
        currency=currency,
        customer_email=os.getenv('ACCOUNT_EMAIL'),
        customer_name='John Doe',
        customer_phone='0778000111'
    )

    payment.add(CartItem(f'TestItem-{randint(1, 99)}', float(amount)))

    # express checkout
    response = api.initiate_express(payment, PaymentMethod.ONEMONEY, test_mode=TestMode.SUCCESS)

    # web transaction
    # response = api.initiate_web(payment)

    pprint(response)
    print("Was transaction paid? ", response.is_paid)

    if response.poll_url:
        poll(response.poll_url)

print('Running Paynow SDK Test...\n')

test()

# url = 'https://www.paynow.co.zw/Interface/CheckPayment/?guid=1e31ae05-f108-45ec-aacf-85d89c59669a'
# poll(url)

# txn_trace_ref = "txn-trace-6759"
# trace_txn(txn_trace_ref)

print('\nTest Completed.')