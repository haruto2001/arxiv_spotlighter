__all__ = ["SlackNotifier"]


import json
import requests
from requests import Response
from requests.exceptions import RequestException


class SlackNotifier:
    """
    A class to send notifications to a Slack channel via a webhook.

    Attributes:
        webhook_url (str): The URL of the Slack webhook.
        channel (str): The Slack channel to send the notification to.
        username (str): The username that will appear as the sender of the notification.
        icon (str): The emoji icon that will appear alongside the username.

    Methods:
        notify(text: str, color: str) -> None:
            Sends a notification to the Slack channel with the specified text and color.
    """

    def __init__(self, webhook_url: str, channel: str, username: str, icon: str) -> None:
        """
        Initializes the SlackNotifier with the webhook URL, channel, username, and icon.

        Args:
            webhook_url (str): The URL of the Slack webhook.
            channel (str): The Slack channel to send the notification to.
            username (str): The username that will appear as the sender of the notification.
            icon (str): The emoji icon that will appear alongside the username.
        """
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon = icon

    def notify(self, text: str, color: str) -> None:
        """
        Sends a notification to the Slack channel with the specified text and color.

        Args:
            text (str): The text of the notification.
            color (str): The color of the attachment bar.

        Returns:
            None

        Raises:
            ValueError: If any of the inputs are invalid.
            RequestException: If there is an issue with the HTTP request.
        """
        if not text or not isinstance(text, str):
            raise ValueError("`text` must be a non-empty string.")
        if not color or not isinstance(color, str):
            raise ValueError("`color` must be a non-empty string.")

        payload = {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon,
            "attachments": [{
                "color": color,
                "text": text
            }],
        }

        self._send_request(payload)

    def _send_request(self, payload: dict) -> Response:
        """
        Sends an HTTP POST request with the given payload.

        Args:
            payload (Dict[str, str]): The payload to send in the POST request.

        Returns:
            Response: The response from the POST request.

        Raises:
            RequestException: If there is an issue with the HTTP request.
        """
        try:
            response: Response = requests.post(self.webhook_url, data=json.dumps(payload))
            response.raise_for_status()
            return response
        except RequestException as e:
            raise RequestException(f"Failed to send notification: {e}")
