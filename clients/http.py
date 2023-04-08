import logging
from http import HTTPStatus
from typing import Tuple

import requests

from clients.exceptions import CouldNotConnectException, ClientException, ServerException, InvalidJSONException

logger = logging.getLogger(__name__)


class HTTPClient:
    """A class for making HTTP requests and handling the responses.

    Attributes:
    - timeout (int): the timeout for the requests in seconds

    Methods:
    - get(url: str) -> Tuple[int, dict]: makes a GET request to the specified URL and returns a tuple with the
        status code and the parsed JSON response
    """

    def __init__(self, timeout=10) -> None:
        """Initializes an HTTPClient instance.

        Args:
            - timeout (int): the timeout for the requests in seconds
        """
        self.timeout = timeout

    def get(self, url) -> Tuple[int, dict]:
        """Makes a GET request to the specified URL and returns a tuple with the status code and the parsed JSON
            response.

        Args:
        - url (str): the URL to send the GET request to

        Returns:
        - Tuple[int, dict]: a tuple with the status code and the parsed JSON response

        Raises:
        - CouldNotConnectException: if a timeout occurs while making the request
        - ClientException: if the response status code is a bad request (4xx)
        - ServerException: if the response status code is a server error (5xx)
        - InvalidJSONException: if the response content is not a valid JSON string
        """
        logger.debug(f"Sending GET request to: {url}")

        try:
            response = requests.get(
                url=url,
                timeout=self.timeout,
            )
        except requests.Timeout as error:
            logger.exception("Timeout occurred")
            raise CouldNotConnectException(message=str(error))

        status_code = response.status_code
        extra_log_info = dict(
            url=url,
            status_code=status_code,
            raw_response=response.content[:1024],
        )
        logger.debug(f"Response received", extra=extra_log_info)

        if HTTPStatus.BAD_REQUEST <= status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ClientException(message="Bad request", additional_info=extra_log_info)

        if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ServerException(message="Internal server error", additional_info=extra_log_info)

        try:
            json_response = response.json()
        except requests.JSONDecodeError:
            message = 'Could not decode JSON received'
            logger.exception(message, extra=extra_log_info)
            raise InvalidJSONException(message=message)

        logger.debug(f"Finishing GET request")

        return status_code, json_response
