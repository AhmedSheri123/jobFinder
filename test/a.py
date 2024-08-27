import requests
url = 'https://restapi.paylink.sa{q}'

def auth():
    u = url.format(q="/api/auth")

    data = {
        "apiId":"APP_ID_1681303723036",
        "secretKey":"e6b717d3-62ff-4f8c-a451-4194c2c5d55a",
        "persistToken":"false"
    }

    r = requests.post(u, json=data)
    return r.json()

def DoPay(orderID, total_price_amount, email, phone, clientName, expiry_month, expiry_year, card_number, CVC, ser_title, ser_disc, callBackUrl):
        
    id_token = auth().get('id_token')
    if id_token:
        u = url.format(q="/api/payInvoice")
        
        data = {
        "amount": total_price_amount,
        "callBackUrl": callBackUrl,
        "clientEmail": email,
        "clientMobile": phone,
        "clientName": clientName,
        "note": ser_disc,
        "orderNumber": orderID,
        "card":{
            "expiry": {
            "month": expiry_month,
            "year": expiry_year
            },
            "number": card_number,
            "securityCode":CVC
        },
        "products": [
            {
            "description": ser_disc,
            "imageSrc": None,
            "isDigital": True,
            "price": total_price_amount,
            "qty": 1,
            "title": ser_title
            }
        ]
        }
        
        headers = {
                "Authorization": f"Bearer {id_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
        }
        r = requests.post(u, headers=headers, json=data)