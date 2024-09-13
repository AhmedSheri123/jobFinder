import requests, json

wa_webhook_secret = '88zByXkTh4Qy3z09XLmJOQWxRYAq3hDD'
wa_instances = 18590

def get_session():
    wa_token = 'JBRvf7YIXBqJHjPgcAVjVLM35T48RHdwrHKdT466d795a1eb'

    s = requests.Session()
    s.headers = {
        'Authorization': f'Bearer {wa_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'eazeWA Webhook User Agent',
    }
    return s


def wa_send_msg(msg='', phone='', dial_code=''):
    
    dial_code = dial_code.replace('+', '')
    num = dial_code+phone
    url = f'https://waapi.app/api/v1/instances/{wa_instances}/client/action/send-message'

    s = get_session()
    payload = {
        "chatId": f"{num}@c.us",
        "message": msg,
    }
    payload_str = json.dumps(payload).encode('UTF-8')
    r = s.post(url=url, data=payload_str)

    if r.json().get('status') == 'success':
        return True
    return False