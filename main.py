import schedule
import time
from datetime import datetime
from dmv_client import DMVClient
from notifier import Notifier
from config import CHECK_INTERVAL_MINUTES

def check_availability():
    """Check for DMV appointment availability and send notification if found."""
    print(f"Checking availability at {datetime.now()}")
    
    client = DMVClient()
    notifier = Notifier()
    
    earliest_appointments = client.get_earliest_appointments()
    if earliest_appointments:
        notifier.send_email_alert(earliest_appointments)

def main():
    # Schedule the job
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(check_availability)
    
    # Run immediately on startup
    check_availability()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 