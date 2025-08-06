import os
from dotenv import load_dotenv

load_dotenv()

# DMV Configuration
DMV_LOCATIONS = {
    # 34: "Brooklyn Atlantic Center",
    35: "Brooklyn Coney Island",
    # 32: "Bronx District Office",
    # 16: "Bronx License Center",
    # 22: "Bethpage",
    # 29: "Garden City",
    # 24: "Massapequa",
    # 30: "Harlem",
    12: "Manhattan License Express",
    25: "Lower Manhattan",
    # 36: "College Point (Queens)",
    # 19: "Jamaica",
    # 33: "Springfield Gardens (Queens)",
    # 31: "Staten Island"
}

DMV_SERVICE_TYPES = {
    # 204: "Upgrade to a REAL ID or Enhanced Driver License (EDL)",
    206: "Change Information on a Photo Document"
}

AVAILABILITY_WINDOW_DAYS = 5  # Only show appointments within this many days

# API Configuration
DMV_API_BASE_URL = "https://publicwebsiteapi.nydmvreservation.com/api" 

# Email Configuration
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
