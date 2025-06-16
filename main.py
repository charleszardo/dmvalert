from datetime import datetime
from dmv_client import DMVClient
from notifier import Notifier

def check_availability():
    """Check for DMV appointment availability and send notification if found."""
    print(f"Checking availability at {datetime.now()}")
    
    client = DMVClient()
    notifier = Notifier()
    
    earliest_appointments = client.get_earliest_appointments()
    if earliest_appointments:
        notifier.send_email_alert(earliest_appointments)

if __name__ == "__main__":
    check_availability() 