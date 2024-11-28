import os
import base64
import json
import requests

MSTEAMS_WEBHOOK = os.getenv("MSTEAMS_WEBHOOK")

def msteam_alert(event, context):
    """
    Sends an alert to MS Teams in case of task success.
    Args:
        event (dict): Event object containing information about the task instance.
        context (dict): Context object containing information about the task instance.
    """

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_json = json.loads(pubsub_message)
    finding = message_json['finding']

    body = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Execution Notification",
        "sections": [
            {
                "activityTitle": f"Google Cloud SCC Alert! - {finding['state']} {finding['category']}",
                "activitySubtitle": f"{finding['severity']} - {message_json['resource']['projectDisplayName']}",
                "activityImage": "https://img.icons8.com/color/high-priority",
                "facts": [
                    {
                        "name": "Finding Class",
                        "value": f"{finding['findingClass']}"
                    },
                    {
                        "name": "Event Time",
                        "value": f"{finding['eventTime']}"
                    },
                    {
                        "name": "Explanation",
                        "value": f"{finding['sourceProperties']['Explanation']}"
                    },
                    {
                        "name": "Recommendation",
                        "value": f"{finding['sourceProperties']['Recommendation']}"
                    }
                ],
            }
        ],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "View Finding",
                "targets": [
                    {
                        "os": "default",
                        "uri": finding['externalUri']
                    }
                ]
            }
        ]
    }

    print("sending alert card")
    _make_http_request(body, MSTEAMS_WEBHOOK)


def _make_http_request(body, full_url):
    """
    Sends an HTTP POST request with the provided body to the given URL.
    Args:
        body (dict): The request body.
        full_url (str): The URL to send the request to.
    """
    r = requests.post(
        url=full_url,
        json=body,
        headers={"Content-type": "application/json"},
        timeout=10,
    )
    print(r.status_code, r.ok)
