# Paynow SDK
Python SDK for Paynow Payment Gateway - sdk that just works!

> This a fork rework of the official Paynow Python SDK

# Why fork?
- Because pull requests are not always merged on time!
- This is a total rework from ground up. The approach i used is different from the official sdk

# Features
- A more modern pythonic approach
- Better project scaffolding
- Get better request output
- Clear variables and responses
- Easy way to test
- Easy support for multicurrencies (multi-integration)
- Query transaction by polling or trace

# Setup

1. Install dependencies
2. Get that money

```bash
$ pip install git+https://github.com/DonnC/paynow-sdk.git
```

# Multi Currency Support
To support for multi currency, Paynow requires that you create each integration keys per currency.
To support this, this project allows you to configure either a single config or multiple configs with different keys and currencies. 
> The config to be used will be determined by the transaction request currency.

# Usage
Check more in [example.py](example.py)

I assume you have your a `.env` with the below keys in it for the example

```python
import os
from pprint import pprint

from paynow_sdk import Paynow, PaynowConfig, Payment, PaymentMethod

# your server endpoints to handle redirects and results
redirect_on_success_callback_url = "http://localhost:8000/api/redirect"
transaction_update_callback_url  = "http://localhost:8000/api/update"

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

currency="USD"
txn_ref = str(uuid.uuid4())
txn_trace = "txn-trace-" + str(randint(1000, 9999))

print(f'Initiating Test Payment with Reference: {txn_ref} for Amount: {amount}\n')

payment = Payment(
        merchant_reference=txn_ref,
        merchant_trace=txn_trace,
        currency=currency,
        customer_email=os.getenv('ACCOUNT_EMAIL'),
)

payment.add(CartItem('Netflix Subscription', 5.00))

# 1. Express transaction: for money wallet + any other supported types
response = api.initiate_express(
    payment, 
    PaymentMethod.INNBUCKS, 

    # test different scenarios in test mode
    # set to None or don't set at all when in prod
    test_mode=TestMode.SUCCESS
)

# 2. Web transaction
#response = api.initiate_web(payment)

pprint(response)

print("Transaction has been paid? ", response.is_paid)


# Poll url
if response.poll_url:
    poll_response = api.poll_url(response.poll_url)
    print("Poll response")
    pprint(poll_response)
```

### Query transaction
You can get transaction status by `poll url` (the usual) or using `merchant trace`.

To get status by poll url, simply call the `api.poll_url(<url>)` from the poll url you received when you initiated the transaction. 

Another approach is to use the `trace number`. This will only work if you send your transactions with this trace number `(like as in the example)`. You can then call `api.trace_transaction(<txn-trace-no>, <txn-currency>)` passing your merchant trace number and the transaction currency used on that transaction trace.

> All responses will return the same `PaymentResponse` model

### Usage Response
All api calls return the same unified response structure.
Check the [model here](paynow_sdk/models.py)

Example output responses of `pprint(response)` are as below

```bash
# Attempt with an unsupported method
PaymentResponse(upstream_data={'error': 'The ID specified is currently in test '
                                        'mode. This is not permitted for '
                                        'remote InnBucks transactions',
                               'status': 'Error'},
                success=False,
                message='The ID specified is currently in test mode. This is '
                        'not permitted for remote InnBucks transactions',
                hash=None,
                token=None,
                merchant_reference='915a9a15-b357-4572-998f-598bbf9dd068',
                status=None,
                redirect_url=None,
                poll_url=None,
                gateway_reference=None,
                gateway_guid=None,
                instructions=None,
                amount=None)

# Express test transaction success
PaymentResponse(upstream_data={'hash': '092D1B28ED0C988C68FE8898C39A54CCC60DE582A3508367DE346436F68847525D014E9E2BF8D4E17C3B1AF252EFB7350C1BD97C830F98DD1A3D30C523C21DC8',
                               'instructions': 'This is a test transaction. '
                                               'Test Case: Success',
                               'paynowreference': '36225925',
                               'pollurl': 'https://www.paynow.co.zw/Interface/CheckPayment/?guid=23768faf-2075-46a3-a464-855a47efb392',
                               'status': 'Ok'},
                success=True,
                message='This is a test transaction. Test Case: Success',
                hash='092D1B28ED0C988C68FE8898C39A54CCC60DE582A3508367DE346436F68847525D014E9E2BF8D4E17C3B1AF252EFB7350C1BD97C830F98DD1A3D30C523C21DC8',
                token=None,
                merchant_reference='cda65270-1f00-4141-a437-193db3f514ae',
                status='Ok',
                redirect_url=None,
                poll_url='https://www.paynow.co.zw/Interface/CheckPayment/?guid=23768faf-2075-46a3-a464-855a47efb392',
                gateway_reference='36225925',
                gateway_guid='23768faf-2075-46a3-a464-855a47efb392',
                instructions='This is a test transaction. Test Case: Success',
                amount=None
                )


# Web transaction
PaymentResponse(upstream_data={'browserurl': 'https://www.paynow.co.zw/Payment/ConfirmPayment/36226393/donychinhuru@gmail.com//',
                               'hash': '00292510B9EBDEE97FABA6291689627FC95F6C653A4A69C19C5C9D66B6085249DB0B82069FEF9C2708BD61BC01FF3FF93F0BFF4C35E3E69FF9DAE343B13867AF',
                               'pollurl': 'https://www.paynow.co.zw/Interface/CheckPayment/?guid=1e31ae05-f108-45ec-aacf-85d89c59669a',
                               'status': 'Ok'},
                success=True,
                message='Payment Status: Ok',
                hash='00292510B9EBDEE97FABA6291689627FC95F6C653A4A69C19C5C9D66B6085249DB0B82069FEF9C2708BD61BC01FF3FF93F0BFF4C35E3E69FF9DAE343B13867AF',
                token=None,
                merchant_reference='e9f7f2cc-2e71-4976-929a-463b5b784618',
                status='Ok',
                redirect_url='https://www.paynow.co.zw/Payment/ConfirmPayment/36226393/donychinhuru@gmail.com//',
                poll_url='https://www.paynow.co.zw/Interface/CheckPayment/?guid=1e31ae05-f108-45ec-aacf-85d89c59669a',
                gateway_reference='36226393',
                gateway_guid='1e31ae05-f108-45ec-aacf-85d89c59669a',
                instructions='Please proceed to: '
                             'https://www.paynow.co.zw/Payment/ConfirmPayment/36226393/donychinhuru@gmail.com// '
                             'to complete the payment.',
                amount=1.5)


# Poll url / trace response 1
PaymentResponse(upstream_data={'amount': '1.50',
                               'hash': 'F9CD825832C9B673027EA90D04A27C3B3C91D880A2AD8C4B8A5EA74B8C56C1817C115011F154AD39981C8C856C3298616F4707CB84509C2606E5B3EDFB284B47',
                               'paynowreference': '36225925',
                               'pollurl': 'https://www.paynow.co.zw/Interface/CheckPayment/?guid=23768faf-2075-46a3-a464-855a47efb392',
                               'reference': 'cda65270-1f00-4141-a437-193db3f514ae',
                               'status': 'Sent'},
                success=True,
                message='Payment Status: Sent',
                hash='F9CD825832C9B673027EA90D04A27C3B3C91D880A2AD8C4B8A5EA74B8C56C1817C115011F154AD39981C8C856C3298616F4707CB84509C2606E5B3EDFB284B47',
                token=None,
                merchant_reference='cda65270-1f00-4141-a437-193db3f514ae',
                status='Sent',
                redirect_url=None,
                poll_url='https://www.paynow.co.zw/Interface/CheckPayment/?guid=23768faf-2075-46a3-a464-855a47efb392',
                gateway_reference='36225925',
                gateway_guid='23768faf-2075-46a3-a464-855a47efb392',
                instructions=None,
                amount=1.5)


# Poll / trace response 2
PaymentResponse(upstream_data={'amount': '1.50',
                               'hash': '2144DA3537101A61D9174A76AF9EF85AFD1F2BB5E170B990CDF1853593658AF36822A5BFAF56B8A0D0E35491DA266F28CD1E846D0E7EF5664DDECE1424D1D523',
                               'paynowreference': '36225925',
                               'pollurl': 'https://www.paynow.co.zw/Interface/CheckPayment/?guid=23768faf-2075-46a3-a464-855a47efb392',
                               'reference': 'cda65270-1f00-4141-a437-193db3f514ae',
                               'status': 'Paid'},
                success=True,
                message='Payment Status: Paid',
                hash='2144DA3537101A61D9174A76AF9EF85AFD1F2BB5E170B990CDF1853593658AF36822A5BFAF56B8A0D0E35491DA266F28CD1E846D0E7EF5664DDECE1424D1D523',
                token=None,
                merchant_reference='cda65270-1f00-4141-a437-193db3f514ae',
                status='Paid',
                redirect_url=None,
                poll_url='https://www.paynow.co.zw/Interface/CheckPayment/?guid=23768faf-2075-46a3-a464-855a47efb392',
                gateway_reference='36225925',
                gateway_guid='23768faf-2075-46a3-a464-855a47efb392',
                instructions=None,
                amount=1.5)
```
