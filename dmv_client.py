import requests
from datetime import datetime, timedelta
from config import (
    DMV_API_BASE_URL, 
    DMV_LOCATIONS, 
    DMV_SERVICE_TYPES,
    AVAILABILITY_WINDOW_DAYS
)
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class DMVClient:
    def __init__(self):
        self.base_url = DMV_API_BASE_URL
        self.session = self._create_session()

    def _create_session(self):
        """Create a requests session with retry logic."""
        session = requests.Session()
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Add browser-like headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://dmv.ny.gov/',
            'Origin': 'https://dmv.ny.gov',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        
        return session

    def _is_within_time_window(self, date_str):
        """Check if the appointment date is within the configured time window."""
        try:
            appointment_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            now = datetime.now()
            window_end = now + timedelta(days=AVAILABILITY_WINDOW_DAYS)
            return now <= appointment_date <= window_end
        except (ValueError, TypeError):
            return False

    def get_availability_for_location(self, location_id, service_type_id):
        """Get available appointments for a specific location and service type."""
        url = f"{self.base_url}/AvailableLocationDates"
        params = {
            "locationId": location_id,
            "typeId": service_type_id,
            "startDate": datetime.utcnow().isoformat() + "Z"
        }
        
        location_name = DMV_LOCATIONS[location_id]
        print(f"Checking {location_name}...")
        
        try:
            time.sleep(0.2)
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data and "LocationAvailabilityDates" in data:
                filtered_dates = []
                for date_info in data["LocationAvailabilityDates"]:
                    if self._is_within_time_window(date_info["AvailabilityDate"]):
                        filtered_dates.append(date_info)
                data["LocationAvailabilityDates"] = filtered_dates
                
                if filtered_dates:
                    data["FirstAvailableDate"] = filtered_dates[0]["AvailabilityDate"]
                else:
                    data["FirstAvailableDate"] = None
                
                print(f"Found {len(filtered_dates)} available dates for {location_name}")
            
            return {
                'location_id': location_id,
                'location_name': location_name,
                'service_type': DMV_SERVICE_TYPES[service_type_id],
                'data': data
            }
        except requests.Timeout:
            print(f"Timeout while checking {location_name}")
            return None
        except requests.RequestException as e:
            print(f"Error checking {location_name}: {str(e)}")
            return None

    def get_all_availability(self):
        """Get available appointments for all configured locations and service types in parallel."""
        results = []
        
        # Reduce concurrent requests further
        max_workers = 3
        
        print(f"\nChecking {len(DMV_LOCATIONS)} locations with {max_workers} workers...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_location = {
                executor.submit(
                    self.get_availability_for_location,
                    location_id,
                    service_type_id
                ): (location_id, service_type_id)
                for location_id in DMV_LOCATIONS.keys()
                for service_type_id in DMV_SERVICE_TYPES.keys()
            }
            
            for future in as_completed(future_to_location):
                result = future.result()
                if result:
                    results.append(result)
        
        print(f"\nCompleted checking all locations. Found results for {len(results)} location-service combinations.")
        return results

    def get_earliest_appointments(self):
        """Get the earliest available appointment for each location and service type within the time window."""
        availability_data = self.get_all_availability()
        earliest_appointments = []
        
        for location_data in availability_data:
            if location_data and location_data['data']:
                earliest_date = location_data['data'].get("FirstAvailableDate")
                if earliest_date and self._is_within_time_window(earliest_date):
                    earliest_appointments.append({
                        'location_name': location_data['location_name'],
                        'service_type': location_data['service_type'],
                        'earliest_date': earliest_date
                    })
        
        # Sort appointments by date
        earliest_appointments.sort(key=lambda x: x['earliest_date'])
        return earliest_appointments 