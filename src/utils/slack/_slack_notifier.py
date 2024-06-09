__all__ = ["SlackNotifierConfig", "SlackNotifier"]


import json
import logging
import requests
from dataclasses import dataclass
from requests import Response
from requests.exceptions import RequestException
from typing import Callable, Dict, Optional


logger = logging.getLogger(__name__)


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
        requester (Optional[Callable[[str, Dict], Response]]): Function to send HTTP POST requests.

    Methods:
        run(text: str, color: str = "#36a64f") -> None:
            Sends a notification to the Slack channel with the specified text and color.
    """

    def __init__(
        self,
        config: SlackNotifierConfig,
        requester: Optional[Callable[[str, Dict], Response]] = None
    ) -> None:
        """Initializes the SlackNotifier with the webhook URL, username, and icon.

        Args:
            config (SlackNotifierConfig): Configuration object with webhook_url, username, and icon.
            requester (Optional[Callable[[str, Dict], Response]]): Function to send HTTP POST requests.
        """
        self.webhook_url = config.webhook_url
        self.username = config.username
        self.icon = config.icon
        self.requester = requester if requester is not None else requests.post

    def _validate_args(self, text: str, color: str) -> None:
        """Validates the input arguments for the run method.

        Args:
            text (str): The text of the notification.
            color (str): The color of the attachment bar.

        Raises:
            ValueError: If any of the inputs are invalid.
        """
        if not text or not isinstance(text, str):
            raise ValueError("`text` must be a non-empty string.")
        if not color or not isinstance(color, str):
            raise ValueError("`color` must be a non-empty string.")

    def _make_payload(self, text: str, color: str) -> dict:
        """Constructs the payload for the Slack notification.

        Args:
            text (str): The text of the notification.
            color (str): The color of the attachment bar.

        Returns:
            dict: The payload to send in the POST request.
        """
        payload = {
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
            response: Response = self.requester(self.webhook_url, data=json.dumps(payload))
            response.raise_for_status()
            logger.info("Notification sent successfully")
            return response
        except RequestException as e:
            logger.error(f"Failed to send notification: {e}")
            raise RequestException(f"Failed to send notification: {e}")

    def run(self, text: str, color: str = "#36a64f") -> None:
        """Sends a notification to the Slack channel with the specified text and color.

        Args:
            text (str): The text of the notification.
            color (str): The color of the attachment bar. Default is "#36a64f".

        Returns:
            None

        Raises:
            ValueError: If any of the inputs are invalid.
            RequestException: If there is an issue with the HTTP request.
        """
        self._validate_args(text, color)
        payload = self._make_payload(text, color)
        self._send_request(payload)
