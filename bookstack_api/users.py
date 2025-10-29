"""Users management for BookStack API."""

from typing import List, Dict, Any, Optional


class UsersManager:
    """Manager for BookStack Users operations."""

    def __init__(self, client):
        """Initialize with BookStack client."""
        self.client = client

    def list(
        self,
        count: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        List all users.

        Args:
            count: Number of items to return
            offset: Offset for pagination
            sort: Sort field
            filter: Filter dictionary

        Returns:
            List of users
        """
        params = {}
        if count is not None:
            params["count"] = count
        if offset is not None:
            params["offset"] = offset
        if sort:
            params["sort"] = sort
        if filter:
            for key, value in filter.items():
                params[f"filter[{key}]"] = value

        response = self.client.get("users", params=params)
        return response.get("data", [])

    def get(self, user_id: int) -> Dict[str, Any]:
        """
        Get a specific user by ID.

        Args:
            user_id: User ID

        Returns:
            User data
        """
        response = self.client.get(f"users/{user_id}")
        return response

    def create(
        self,
        name: str,
        email: str,
        password: Optional[str] = None,
        send_invite: Optional[bool] = None,
        language: Optional[str] = None,
        roles: Optional[List[int]] = None,
        external_auth_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            name: User's full name
            email: User's email address
            password: User's password (if not sending invite)
            send_invite: Send invitation email
            language: User's language preference (e.g., 'de', 'en')
            roles: List of role IDs to assign
            external_auth_id: External authentication ID
            **kwargs: Additional fields

        Returns:
            Created user data
        """
        data = {
            "name": name,
            "email": email,
            **kwargs,
        }

        if password is not None:
            data["password"] = password
        if send_invite is not None:
            data["send_invite"] = send_invite
        if language is not None:
            data["language"] = language
        if roles is not None:
            data["roles"] = roles
        if external_auth_id is not None:
            data["external_auth_id"] = external_auth_id

        response = self.client.post("users", json_data=data)
        return response

    def update(
        self,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        language: Optional[str] = None,
        roles: Optional[List[int]] = None,
        external_auth_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Update an existing user.

        Args:
            user_id: User ID
            name: New user name
            email: New email address
            password: New password
            language: New language preference
            roles: New list of role IDs
            external_auth_id: New external auth ID
            **kwargs: Additional fields to update

        Returns:
            Updated user data
        """
        data = {**kwargs}

        if name is not None:
            data["name"] = name
        if email is not None:
            data["email"] = email
        if password is not None:
            data["password"] = password
        if language is not None:
            data["language"] = language
        if roles is not None:
            data["roles"] = roles
        if external_auth_id is not None:
            data["external_auth_id"] = external_auth_id

        response = self.client.put(f"users/{user_id}", json_data=data)
        return response

    def delete(self, user_id: int, migrate_ownership_id: Optional[int] = None) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID to delete
            migrate_ownership_id: User ID to migrate content ownership to

        Returns:
            True if successful
        """
        params = {}
        if migrate_ownership_id is not None:
            params["migrate_ownership_id"] = migrate_ownership_id

        self.client.delete(f"users/{user_id}")
        return True
