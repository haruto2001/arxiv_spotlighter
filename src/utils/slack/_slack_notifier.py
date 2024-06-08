__all__ = ["SlackNotifierConfig", "SlackNotifier"]


import json
import requests
from dataclasses import dataclass
from requests import Response
from requests.exceptions import RequestException


@dataclass
class SlackNotifierConfig:
    """Configuration class for SlackNotifier.

    Attributes:
        webhook_url (str): The URL of the Slack webhook.
        username (str): The username that will appear as the sender of the notification.
        icon (str): The emoji icon that will appear alongside the username.
    """
    webhook_url: str
    username: str = "ArxivSpotlighter"
    icon: str = ":+1:"


class SlackNotifier:
    """A class to send notifications to a Slack channel via a webhook.

    Attributes:
        webhook_url (str): The URL of the Slack webhook.
        username (str): The username that will appear as the sender of the notification.
        icon (str): The emoji icon that will appear alongside the username.

    Methods:
        notify(text: str, color: str) -> None:
            Sends a notification to the Slack channel with the specified text and color.
    """

    def __init__(self, config: SlackNotifierConfig) -> None:
        """Initializes the SlackNotifier with the webhook URL, username, and icon.

        Args:
            config (SlackNotifierConfig): Configuration object with webhook_url, username, and icon.
        """
        self.webhook_url = config.webhook_url
        self.username = config.username
        self.icon = config.icon

    def _make_payload(self, text: str, color: str) -> dict:
        """Constructs the payload for the Slack notification.

        Args:
            text (str): The text of the notification.
            color (str): The color of the attachment bar.

        Returns:
            dict: The payload to send in the POST request.
        """
        payload = {
            # "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon,
            "attachments": [{
                "color": color,
                "text": text
            }],
        }
        return payload

    def _send_request(self, payload: dict) -> Response:
        """Sends an HTTP POST request with the given payload.

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

    def run(self, text: str, color: str) -> None:
        """Sends a notification to the Slack channel with the specified text and color.

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
        payload = self._make_payload(text, color)
        self._send_request(payload)
