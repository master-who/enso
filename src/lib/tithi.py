

import requests
import json
from datetime import datetime

import notify

url = "https://json.freeastrologyapi.com/tithi-durations"
api_key = "uR2DuV2dxH7Quh48uBjf11TAGP2ZTkSc3xBf1nbg"
subscriptions = [
    {'endpoint': 'https://fcm.googleapis.com/fcm/send/cfzwE1V4jlM:APA91bEuOi4Bv_W4Ahg3713nfqJ06VHRkf5ktrnyog5PCYXW3Fs1efiML5EF2pBi0Kne41raeNrNtAPoksxTYGRmbu4GY0-B8fZSn1eE7Cv30r3pOJVq4OPgObvJyxiujywvCndMUiNP', 'expirationTime': None, 'keys': {'p256dh': 'BM9QAEApa_vRxebni7Ok8WnZmCA_WChADMx45OL_46v7BZYRBmT4rQjxOxnAFEH1ZGMm1YBfD4nQr97e4gfdYpM', 'auth': 'l-Db4nt0J6mewzFjBEq0NQ'}}
]

def notify_today(schedule):
    now = datetime.now()

    payload = json.dumps({
        "year": now.year,
        "month": now.month,
        "date": now.day,
        "hours": now.hour,
        "minutes": now.minute,
        "seconds": now.second,
        "latitude": 16.4318209,
        "longitude": 80.5688069,
        "timezone": 5.5,
        "config": {
            "observation_point": "topocentric",
            "ayanamsha": "lahiri"
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    """
    Example response:
    {
        "number":29,
        "name":"Chaturdashi",
        "paksha":"krishna",
        "completes_at":"2023-03-21 00:28:30",
        "left_precentage":88.55
    }
    """

    data = json.loads(response.json()['output'])

    completion_time = datetime.strptime(data['completes_at'], '%Y-%m-%d %H:%M:%S')
    formatted_time = completion_time.strftime('%I:%M %p - %B %d')

    message = f"{data['name']} till {formatted_time}"

    for s in subscriptions:
        notify.push_message(s, message)
