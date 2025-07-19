from pywebpush import webpush, WebPushException

def push_message(subscription, message):
    VAPID_PRIVATE_KEY = "1YvkmFA5p31EK31c6GYQ79Ev__ozsoGOJNBmdMomIp8"
    VAPID_CLAIMS = { "sub": "mailto:none@masterwho.in" }

    print(f"Sending message: {message} to subscription: {subscription['endpoint']}")
    webpush(
        subscription,
        data=message,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )
