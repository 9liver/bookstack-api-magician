"""Main BookStack API client."""

import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from .exceptions import (
    BookStackAPIError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    PermissionError,
    RateLimitError,
)
from .shelves import ShelvesManager
from .books import BooksManager
from .chapters import ChaptersManager
from .pages import PagesManager
from .users import UsersManager


class BookStackClient:
    """Main client for interacting with BookStack API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token_id: Optional[str] = None,
        token_secret: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True,
    ):
        """
        Initialize BookStack API client.

        Args:
            base_url: BookStack instance URL
            token_id: API token ID
            token_secret: API token secret
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        # Load from environment if not provided
        load_dotenv()

        self.base_url = (base_url or os.getenv("BOOKSTACK_URL", "")).rstrip("/")
        self.token_id = token_id or os.getenv("BOOKSTACK_TOKEN_ID")
        self.token_secret = token_secret or os.getenv("BOOKSTACK_TOKEN_SECRET")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not all([self.base_url, self.token_id, self.token_secret]):
            raise AuthenticationError(
                "Missing credentials. Provide base_url, token_id, and token_secret "
                "or set BOOKSTACK_URL, BOOKSTACK_TOKEN_ID, and BOOKSTACK_TOKEN_SECRET "
                "environment variables."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.token_id}:{self.token_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        # Initialize resource managers
        self.shelves = ShelvesManager(self)
        self.books = BooksManager(self)
        self.chapters = ChaptersManager(self)
        self.pages = PagesManager(self)
        self.users = UsersManager(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to BookStack API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            data: Form data
            json_data: JSON data

        Returns:
            Response data as dictionary

        Raises:
            BookStackAPIError: On API errors
        """
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )

            # Handle different status codes
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Check your credentials.",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 403:
                raise PermissionError(
                    "Permission denied.",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 404:
                raise ResourceNotFoundError(
                    "Resource not found.",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 422:
                error_msg = "Validation error."
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg = error_data["message"]
                    elif "error" in error_data:
                        error_msg = error_data["error"]
                except:
                    pass
                raise ValidationError(
                    error_msg,
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded.",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code >= 400:
                error_msg = f"API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg = error_data["message"]
                    elif "error" in error_data:
                        error_msg = error_data["error"]
                except:
                    pass
                raise BookStackAPIError(
                    error_msg,
                    status_code=response.status_code,
                    response=response,
                )

            # Parse response
            if response.status_code == 204:  # No content
                return {}

            try:
                return response.json()
            except ValueError:
                return {"data": response.text}

        except requests.exceptions.Timeout:
            raise BookStackAPIError("Request timeout.")
        except requests.exceptions.ConnectionError:
            raise BookStackAPIError("Connection error. Check your base_url.")
        except requests.exceptions.RequestException as e:
            raise BookStackAPIError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make POST request."""
        return self._request("POST", endpoint, data=data, json_data=json_data)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return self._request("PUT", endpoint, data=data, json_data=json_data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._request("DELETE", endpoint)

    def test_connection(self) -> bool:
        """
        Test API connection and credentials.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to list books as a connection test
            self.get("books")
            return True
        except Exception:
            return False
