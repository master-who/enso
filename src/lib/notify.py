import json
from pathlib import Path
from pywebpush import webpush, WebPushException

# Constants
VAPID_PRIVATE_KEY = "1YvkmFA5p31EK31c6GYQ79Ev__ozsoGOJNBmdMomIp8"
VAPID_CLAIMS = { "sub": "mailto:none@masterwho.in" }
SUBSCRIPTIONS_FILE = Path(__file__).parent / "subscriptions.json"

def ensure_subscriptions_file():
    """Ensure subscriptions.json exists with empty structure"""
    if not SUBSCRIPTIONS_FILE.exists():
        with open(SUBSCRIPTIONS_FILE, 'w') as f:
            json.dump({}, f, indent=2)

def load_subscriptions():
    """Load all subscriptions from file"""
    ensure_subscriptions_file()
    with open(SUBSCRIPTIONS_FILE) as f:
        return json.load(f)

def push_message(subscription, message):
    """Send a push notification to a single subscription"""
    print(f"Sending message: {message} to subscription: {subscription['endpoint']}")
    webpush(
        subscription,
        data=message,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )

def push(key, message):
    """Send a push notification to all subscriptions under a specific key"""
    subscriptions = load_subscriptions()
    if key not in subscriptions:
        print(f"No subscriptions found for key: {key}")
        return 0
        
    success_count = 0
    for subscription in subscriptions[key]:
        try:
            push_message(subscription, message)
            success_count += 1
        except Exception as e:
            print(f"Failed to send notification: {e}")
    
    return success_count
