# Google Chronicle Outage Monitor and Webhook Alert

This Python script monitors the Google Cloud Status page for Chronicle Security outages and sends alerts to a Chronicle SOAR webhook.

## Prerequisites

* Python 3: Make sure you have Python 3 installed on your system.
* requests library: Install the `requests` library using `pip install requests`.
* Chronicle SOAR webhook: Set up a webhook endpoint in your Chronicle SOAR instance capable of receiving and processing JSON payloads.

## Setup

1. Clone or download this repository: Get a copy of the code on your local machine.
2. Replace the webhook URL: In the `gcp_outage_checker.py` file, replace the placeholder `https://yourtenant.siemplify-soar.com/webhooks/yourwebhook` with your actual Chronicle SOAR webhook URL.
3. Set up a schedule: Use a task scheduler to run the `gcp_outage_checker.py` script hourly.
   * Linux/macOS: Use cron. Example cron entry:

```
0 * * * * /path/to/python3 /path/to/gcp_outage_checker.py 
```

## How it Works

* The script fetches incident data from the Google Cloud Status page (`https://status.cloud.google.com/incidents.json`).
* It looks for incidents where:
    * `service_name` is "Chronicle Security".
    * The incident's `created` timestamp is within the past two hours.
* If a matching incident is found, the script constructs a JSON payload with the following fields:
    * `TicketID`: Randomly generated UUID
    * `SourceSystemName`: "Google Chronicle"
    * `Name`: "Chronicle Outage"
    * `DeviceVendor`: "Google"
    * `RuleGenerator`: "ChronicleOutage"
    * `StartTime`: Incident's created timestamp
    * `Description`: "There is a Chronicle outage, please review https://status.cloud.google.com/summary for outage details."
* The script sends the JSON payload to your specified Chronicle SOAR webhook, triggering an alert.

## Customization

The `gcp_outage_checker.py` script can be further customized to fit your specific needs. For example, you could adjust:

`LOOKBACK_HOURS` for the time window of outage detection
The JSON payload to include additional fields relevant to your Chronicle SOAR workflow.
