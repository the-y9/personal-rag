from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request
import os
import json

import requests

router = APIRouter()
DATA_FILE = os.path.join(os.path.dirname(__file__), "visitors.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@router.get("/log")
async def log_visitor(request: Request):
    ip = request.headers.get("X-Forwarded-For", request.client.host)
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        print(1, response.json())
        location_data = response.json()
        location = f"{location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}"
        tz = location_data.get('timezone', 'Unknown')
    except Exception as e:
        pass

    data = load_data()
    visitor_record = next((item for item in data if item['ip'] == ip), None)
    if visitor_record:
        visitor_record['visits'] += 1
        visitor_record['last_visited'] = str(datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat())
        visitor_record['location'] = location
        visitor_record['timezone'] = tz

    else:
        visitor_record = {
            "ip": ip,
            "visits": 1,
            "last_visited": str(datetime.now(timezone((timedelta(hours=5, minutes=30)))).isoformat()),
            'location': location,
            'timezone': tz
        }
        data.append(visitor_record)
    
    save_data(data)

    visitor_data = next((item for item in data if item['ip'] == ip), None)
    
    return visitor_data
