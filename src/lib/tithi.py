

import requests
import json
from datetime import datetime
from pathlib import Path
from . import notify

# Constants
url = "https://json.freeastrologyapi.com/tithi-durations"
TODAY_JSON = Path(__file__).parent / "today.json"
api_key = "uR2DuV2dxH7Quh48uBjf11TAGP2ZTkSc3xBf1nbg"


def fetch_current_tithi():
    """Fetch current tithi from the API"""
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
    data = json.loads(response.json()['output'])
    
    return {
        "tithi": data['name'],
        "paksha": data['paksha'],
        "till": data['completes_at']
    }


def load_cached_tithi():
    """Load cached tithi from today.json"""
    try:
        if not TODAY_JSON.exists():
            return None
        
        with open(TODAY_JSON) as f:
            data = json.load(f)
            # Convert string to datetime for comparison
            data['till'] = datetime.strptime(data['till'], '%Y-%m-%d %H:%M:%S')
            return data
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def save_tithi_cache(tithi_data):
    """Save tithi data to today.json"""
    # Ensure till is string for JSON serialization
    if isinstance(tithi_data['till'], datetime):
        tithi_data['till'] = tithi_data['till'].strftime('%Y-%m-%d %H:%M:%S')
    
    with open(TODAY_JSON, 'w') as f:
        json.dump(tithi_data, f, indent=2)


def get_today_tithi():
    """
    Get today's tithi, using cached data if valid.
    Returns dict with tithi info and completion time.
    """
    now = datetime.now()

    # Try to load cached tithi
    cached_data = load_cached_tithi()
    
    # Determine if we need to fetch new data
    if cached_data and now < cached_data['till']:
        print("Using cached tithi data")
        return cached_data
    
    # Fetch new data if needed
    print("Fetching new tithi data from API")
    tithi_data = fetch_current_tithi()
    save_tithi_cache(tithi_data)
    return tithi_data


def format_tithi_message(tithi_data):
    """Format a tithi notification message"""
    completion_time = (
        tithi_data['till'] 
        if isinstance(tithi_data['till'], datetime)
        else datetime.strptime(tithi_data['till'], '%Y-%m-%d %H:%M:%S')
    )
    formatted_time = completion_time.strftime('%I:%M %p - %B %d')
    return f"{tithi_data['tithi']} till {formatted_time}"


def notify_today(schedule):
    """Send push notifications about today's tithi"""
    now = datetime.now()
    print(f"Daily Tithi @ {now.strftime('%Y-%m-%d %H:%M:%S')}")

    tithi_data = get_today_tithi()
    message = format_tithi_message(tithi_data)

    # Send notifications
    sent_count = notify.push('tithi', message)
    print(f"Notifications sent: {sent_count}")
