import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# DMV Configuration
DMV_LOCATIONS = {
    34: "Brooklyn Atlantic Center",
    35: "Brooklyn Coney Island",
    32: "Bronx District Office",
    16: "Bronx License Center",
    22: "Bethpage",
    29: "Garden City",
    24: "Massapequa",
    30: "Harlem",
    12: "Manhattan License Express",
    25: "Lower Manhattan",
    36: "College Point (Queens)",
    19: "Jamaica",
    33: "Springfield Gardens (Queens)",
    31: "Staten Island"
}

DMV_SERVICE_TYPES = {
    204: "Upgrade to a REAL ID or Enhanced Driver License (EDL)"
}

# Time window configuration
CHECK_INTERVAL_MINUTES = 10
AVAILABILITY_WINDOW_DAYS = 5  # Only show appointments within this many days

# Twilio Configuration (for SMS)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')

# API Configuration
DMV_API_BASE_URL = "https://publicwebsiteapi.nydmvreservation.com/api" 

# Email Configuration
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')