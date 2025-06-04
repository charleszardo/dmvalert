# DMV Alert

A Python script that monitors New York DMV locations for appointment availability and sends notifications when slots become available. This is particularly useful when trying to schedule an appointment at a busy DMV location.

## Features

- Monitors multiple DMV locations simultaneously
- Configurable time window for availability (default: 5 days)
- Email notifications when appointments become available
- Parallel processing for efficient checking
- Easy to add new locations
- Configurable check frequency

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dmvalert.git
cd dmvalert
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```env
# Email Configuration (for notifications)
EMAIL=your.email@gmail.com
EMAIL_PASSWORD=your_app_password  # Gmail App Password, not your regular password

# Optional: Twilio Configuration (if using SMS notifications)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
YOUR_PHONE_NUMBER=your_phone_number
```

2. Configure DMV locations in `config.py`:
```python
DMV_LOCATIONS = {
    34: "Brooklyn Atlantic Center",
    35: "Brooklyn Coney Island",
    # Add more locations as needed
}
```

3. Adjust time window and check frequency in `config.py`:
```python
CHECK_INTERVAL_MINUTES = 30  # How often to check for availability
AVAILABILITY_WINDOW_DAYS = 10  # Only show appointments within this many days
```

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Check all configured DMV locations for availability
2. Send an email notification if appointments are found within the configured time window
3. Continue checking at the specified interval

## Setting up Gmail for Notifications

To use Gmail for notifications, you'll need to:
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to Google Account → Security
   - Under "2-Step Verification", click "App passwords"
   - Select "Mail" and your device
   - Use the generated 16-character password in your `.env` file

## Available DMV Locations

The script currently monitors these locations:
- Brooklyn Atlantic Center
- Brooklyn Coney Island
- Bronx District Office
- Bronx License Center
- Bethpage
- Garden City
- Massapequa
- Harlem
- Manhattan License Express
- Lower Manhattan
- College Point (Queens)
- Jamaica
- Springfield Gardens (Queens)
- Staten Island

## Adding New Locations

To add a new location:
1. Find the location ID from the DMV website
2. Add it to the `DMV_LOCATIONS` dictionary in `config.py`:
```python
DMV_LOCATIONS = {
    # ... existing locations ...
    NEW_ID: "New Location Name"
}
```

## Contributing

Feel free to submit issues and enhancement requests!
