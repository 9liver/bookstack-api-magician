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
        debug: bool = False,
    ):
        """
        Initialize BookStack API client.

        Args:
            base_url: BookStack instance URL
            token_id: API token ID
            token_secret: API token secret
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            debug: Enable debug output
        """
        # Load from environment if not provided
        load_dotenv()

        self.base_url = (base_url or os.getenv("BOOKSTACK_URL", "")).rstrip("/")
        self.token_id = token_id or os.getenv("BOOKSTACK_TOKEN_ID")
        self.token_secret = token_secret or os.getenv("BOOKSTACK_TOKEN_SECRET")
        self.timeout = timeout

        # SSL verification can be disabled via env var
        ssl_env = os.getenv("BOOKSTACK_VERIFY_SSL", "").lower()
        if ssl_env in ("false", "0", "no"):
            self.verify_ssl = False
        else:
            self.verify_ssl = verify_ssl

        self.debug = debug or os.getenv("DEBUG", "").lower() in ("true", "1", "yes")

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

        if self.debug:
            print(f"[DEBUG] {method} {url}")
            if params:
                print(f"[DEBUG] Params: {params}")
            if json_data:
                print(f"[DEBUG] JSON: {json_data}")

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

        except requests.exceptions.SSLError as e:
            error_msg = f"SSL error: {str(e)}\n\nTry setting verify_ssl=False or set BOOKSTACK_VERIFY_SSL=false in .env"
            if self.debug:
                print(f"[DEBUG] SSL Error: {e}")
            raise BookStackAPIError(error_msg)
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout}s. URL: {url}"
            if self.debug:
                print(f"[DEBUG] Timeout: {url}")
            raise BookStackAPIError(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: Cannot reach {self.base_url}\n"
            error_msg += f"Please check:\n"
            error_msg += f"  1. URL is correct: {self.base_url}\n"
            error_msg += f"  2. BookStack is running and accessible\n"
            error_msg += f"  3. Network/firewall allows connection\n"
            error_msg += f"\nError details: {str(e)}"
            if self.debug:
                print(f"[DEBUG] Connection Error: {e}")
            raise BookStackAPIError(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            if self.debug:
                print(f"[DEBUG] Request Exception: {e}")
            raise BookStackAPIError(error_msg)

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

    def test_connection_detailed(self) -> Dict[str, Any]:
        """
        Test API connection with detailed error information.

        Returns:
            Dictionary with connection status and details
        """
        result = {
            "success": False,
            "base_url": self.base_url,
            "endpoint": f"{self.base_url}/api/books",
            "ssl_verify": self.verify_ssl,
            "error": None,
            "error_type": None,
            "suggestions": []
        }

        # Check if credentials are set
        if not self.base_url:
            result["error"] = "BOOKSTACK_URL not set"
            result["error_type"] = "missing_config"
            result["suggestions"].append("Set BOOKSTACK_URL in .env file")
            return result

        if not self.token_id or not self.token_secret:
            result["error"] = "API credentials not set"
            result["error_type"] = "missing_credentials"
            result["suggestions"].append("Set BOOKSTACK_TOKEN_ID and BOOKSTACK_TOKEN_SECRET in .env")
            return result

        # Try connection
        try:
            response = self.get("books")
            result["success"] = True
            result["message"] = "Connection successful!"
            return result

        except AuthenticationError as e:
            result["error"] = "Authentication failed"
            result["error_type"] = "auth_error"
            result["error_details"] = str(e)
            result["suggestions"].append("Check your API token ID and secret")
            result["suggestions"].append("Verify tokens are active in BookStack")

        except BookStackAPIError as e:
            if "SSL error" in str(e):
                result["error"] = "SSL certificate verification failed"
                result["error_type"] = "ssl_error"
                result["error_details"] = str(e)
                result["suggestions"].append("Add BOOKSTACK_VERIFY_SSL=false to .env for self-signed certs")
                result["suggestions"].append("Or use verify_ssl=False when creating client")

            elif "Connection error" in str(e):
                result["error"] = "Cannot connect to BookStack"
                result["error_type"] = "connection_error"
                result["error_details"] = str(e)
                result["suggestions"].append(f"Verify BookStack is running at {self.base_url}")
                result["suggestions"].append("Check if URL includes http:// or https://")
                result["suggestions"].append("Check firewall/network settings")

            elif "timeout" in str(e).lower():
                result["error"] = "Connection timeout"
                result["error_type"] = "timeout"
                result["error_details"] = str(e)
                result["suggestions"].append("BookStack server may be slow or unreachable")
                result["suggestions"].append("Check network connectivity")

            else:
                result["error"] = "API request failed"
                result["error_type"] = "api_error"
                result["error_details"] = str(e)
                result["suggestions"].append("Check BookStack logs for more details")

        except Exception as e:
            result["error"] = "Unexpected error"
            result["error_type"] = "unknown"
            result["error_details"] = str(e)
            result["suggestions"].append("Enable debug mode for more information")

        return result
