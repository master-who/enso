import requests
import json
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import pytz

def geocode_nominatim(location):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "SunriseSunsetScript/1.0 (your_email@example.com)"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    if not data:
        raise Exception("Location not found.")
    
    lat = float(data[0]['lat'])
    lon = float(data[0]['lon'])
    display_name = data[0]['display_name']
    return lat, lon, display_name

def get_timezone(lat, lon):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=lat, lng=lon)
    if not timezone_name:
        raise Exception("Could not determine timezone.")
    return timezone_name

def fetch_sunrise_sunset(lat, lon, timezone_name, year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    delta = timedelta(days=1)

    results = []

    while start_date < end_date:
        date_str = start_date.strftime('%Y-%m-%d')
        url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lon}&date={date_str}&timezone={timezone_name}"
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data for {date_str}")
            start_date += delta
            continue
        
        data = response.json()
        if data.get("status") != "OK":
            print(f"API error on {date_str}")
            start_date += delta
            continue

        results.append({
            "date": date_str,
            "sunrise": data['results']['sunrise'],
            "sunset": data['results']['sunset']
        })

        start_date += delta

    return results

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    location_name = input("Enter place name (e.g., Mangalagiri): ").strip()
    year_input = input(f"Enter year [{datetime.now().year}]: ").strip()
    year = int(year_input) if year_input else datetime.now().year

    try:
        lat, lon, full_name = geocode_nominatim(location_name)
        print(f"Found: {full_name} → Latitude: {lat}, Longitude: {lon}")
        
        timezone_name = get_timezone(lat, lon)
        print(f"Timezone: {timezone_name}")

        data = fetch_sunrise_sunset(lat, lon, timezone_name, year)
        filename = f"sunrise_sunset_{year}_{location_name.replace(' ', '_')}.json"
        save_to_json(data, filename)
        print(f"Saved data to {filename}")
    except Exception as e:
        print(f"Error: {e}")
