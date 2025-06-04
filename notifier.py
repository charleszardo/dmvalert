from twilio.rest import Client
from config import EMAIL, EMAIL_PASSWORD, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER
from datetime import datetime
import smtplib
from email.message import EmailMessage

class Notifier:
    def __init__(self):
        try:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            self.from_number = TWILIO_PHONE_NUMBER
            self.to_number = YOUR_PHONE_NUMBER
            print(f"Initialized Twilio client with:")
            print(f"From: {self.from_number}")
            print(f"To: {self.to_number}")
        except Exception as e:
            print(f"Error initializing Twilio client: {e}")

    def _format_date(self, date_str):
        """Convert ISO date string to a more readable format."""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.strftime("%B %d, %Y at %I:%M %p")
        except (ValueError, TypeError):
            return date_str

    def send_alert(self, appointments):
        """Print available appointments to console."""
        if not appointments:
            print("No appointments available")
            return
            
        print("\nDMV Appointments Available!")
        print("---------------------------")
        for appt in appointments:
            formatted_date = self._format_date(appt['earliest_date'])
            print(f"{appt['location_name']}: {formatted_date}")
        print("---------------------------\n")

    def send_sms_alert(self, appointments):
        """Send SMS alert about available appointments."""
        if not appointments:
            return
            
        message = "DMV Appointments Available!\n\n"
        for appt in appointments:
            formatted_date = self._format_date(appt['earliest_date'])
            message += f"{appt['location_name']}: {formatted_date}\n"
        
        try:
            print(f"Attempting to send SMS with message: {message}")
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            print(f"SMS sent successfully! Message SID: {message.sid}")
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            print(f"Error type: {type(e)}") 

    def send_email_alert(self, appointments):
        """Send email alert about available appointments."""
        if not appointments:
            return
            
        message = EmailMessage()
        message['Subject'] = "DMV Appointments Available!"
        message['From'] = EMAIL
        message['To'] = EMAIL
        message.set_content(f"DMV Appointments Available!\n\n" + "\n".join([f"{appt['location_name']}: {self._format_date(appt['earliest_date'])}" for appt in appointments]))

        try:
            print(f"Attempting to send email with message: {message}")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL, EMAIL_PASSWORD)
                smtp.send_message(message)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            print(f"Error type: {type(e)}")

