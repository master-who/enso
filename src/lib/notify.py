import json
from pathlib import Path
from pywebpush import webpush, WebPushException

# Constants
VAPID_PRIVATE_KEY = "1YvkmFA5p31EK31c6GYQ79Ev__ozsoGOJNBmdMomIp8"
VAPID_CLAIMS = { "sub": "mailto:none@masterwho.in" }
SUBSCRIPTIONS_FILE = Path(__file__).parent / "subscriptions.json"
SUPPORTED_THREADS = {'tithi'}  # Add new supported threads here

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

def save_subscriptions(subscriptions):
    """Save subscriptions data to file"""
    with open(SUBSCRIPTIONS_FILE, 'w') as f:
        json.dump(subscriptions, f, indent=2)

def subscribe(thread, subscription):
    """
    Add a subscription to a thread. Returns tuple (success, message).
    If thread doesn't exist, creates it.
    Prevents duplicate subscriptions based on endpoint.
    """
    if thread not in SUPPORTED_THREADS:
        return False, f"Thread '{thread}' is not supported"

    subscriptions = load_subscriptions()

    # Initialize thread if it doesn't exist
    if thread not in subscriptions:
        subscriptions[thread] = []

    # Check for duplicate subscription
    for existing in subscriptions[thread]:
        if existing['endpoint'] == subscription['endpoint']:
            return False, "Subscription already exists"

    # Add new subscription
    subscriptions[thread].append(subscription)
    save_subscriptions(subscriptions)
    return True, "Subscription added successfully"

def push_message(subscription, message):
    """Send a push notification to a single subscription"""
    print(f"Sending message: {message} to subscription: {subscription['endpoint']}")
    webpush(
        subscription,
        data=message,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )

def push(thread, message):
    """Send a push notification to all subscriptions under a specific thread"""
    subscriptions = load_subscriptions()
    if thread not in subscriptions:
        print(f"No subscriptions found for thread: {thread}")
        return 0
        
    success_count = 0
    for subscription in subscriptions[thread]:
        try:
            push_message(subscription, message)
            success_count += 1
        except Exception as e:
            print(f"Failed to send notification: {e}")
    
    return success_count
