import json
import requests
from datetime import datetime, timedelta
import uuid

# Constants
STATUS_URL = "https://status.cloud.google.com/incidents.json"
SERVICE_NAME = "Chronicle Security"
LOOKBACK_HOURS = 2
WEBHOOK_URL = "https://yourtenant.siemplify-soar.com/webhooks/yourwebhook"  # Replace with your webhook url

def send_outage_alert(webhook_url, outage_data):
    """Sends an outage alert in JSON format to the specified webhook."""
    response = requests.post(webhook_url, json=outage_data)

    if response.status_code != 200:
        print(f"Error sending webhook alert: {response.status_code}")

def check_for_outage():
    """Checks for Chronicle Security outages within the last 2 hours."""

    # Calculate lookback threshold based on current time and lookback hours
    now = datetime.now()
    lookback_threshold = now - timedelta(hours=LOOKBACK_HOURS)

    # Fetch the incident data from the JSON endpoint
    response = requests.get(STATUS_URL)
    if response.status_code == 200:
        incidents = response.json()
    else:
        print(f"Error fetching incidents: {response.status_code}")
        return

    # Search for matching incidents
    for incident in incidents:
        created_dt = datetime.strptime(incident['created'], "%Y-%m-%dT%H:%M:%S+00:00")
        if incident['service_name'] == SERVICE_NAME and created_dt > lookback_threshold:
            # Found a matching incident within the time window
            outage_data = {
                "TicketID": str(uuid.uuid4()),  # Generate random ID
                "SourceSystemName": "Google Chronicle",
                "Name": "Chronicle Outage",
                "DeviceVendor": "Google",
                "RuleGenerator": "ChronicleOutage",
                "StartTime": incident['created'],  # Use created field
                "Description": "There is a Chronicle SIEM outage, visit https://status.cloud.google.com/summary and search for Chronicle to see the impact.",
		"Priority": "Critical"
            }

            # Send alert to webhook in JSON format
            send_outage_alert(WEBHOOK_URL, outage_data)
            print("Chronicle Security outage alert sent to webhook")
            break  # Can stop searching once you find a match

if __name__ == "__main__":
    check_for_outage()

