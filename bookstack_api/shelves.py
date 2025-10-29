"""Shelves management for BookStack API."""

from typing import List, Dict, Any, Optional
from .models import Shelf


class ShelvesManager:
    """Manager for BookStack Shelves operations."""

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
        List all shelves.

        Args:
            count: Number of items to return
            offset: Offset for pagination
            sort: Sort field (e.g., 'name', '-created_at')
            filter: Filter dictionary (e.g., {'name': 'test'})

        Returns:
            List of shelves
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

        response = self.client.get("shelves", params=params)
        return response.get("data", [])

    def get(self, shelf_id: int) -> Dict[str, Any]:
        """
        Get a specific shelf by ID.

        Args:
            shelf_id: Shelf ID

        Returns:
            Shelf data
        """
        response = self.client.get(f"shelves/{shelf_id}")
        return response

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        books: Optional[List[int]] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new shelf.

        Args:
            name: Shelf name
            description: Shelf description (HTML or Markdown)
            books: List of book IDs to add to shelf
            tags: List of tags (e.g., [{'name': 'category', 'value': 'docs'}])
            **kwargs: Additional fields

        Returns:
            Created shelf data
        """
        data = {
            "name": name,
            **kwargs,
        }

        if description is not None:
            data["description"] = description
        if books is not None:
            data["books"] = books
        if tags is not None:
            data["tags"] = tags

        response = self.client.post("shelves", json_data=data)
        return response

    def update(
        self,
        shelf_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        books: Optional[List[int]] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Update an existing shelf.

        Args:
            shelf_id: Shelf ID
            name: New shelf name
            description: New shelf description
            books: List of book IDs
            tags: List of tags
            **kwargs: Additional fields to update

        Returns:
            Updated shelf data
        """
        data = {**kwargs}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if books is not None:
            data["books"] = books
        if tags is not None:
            data["tags"] = tags

        response = self.client.put(f"shelves/{shelf_id}", json_data=data)
        return response

    def delete(self, shelf_id: int) -> bool:
        """
        Delete a shelf.

        Args:
            shelf_id: Shelf ID

        Returns:
            True if successful
        """
        self.client.delete(f"shelves/{shelf_id}")
        return True

    def export_html(self, shelf_id: int) -> str:
        """
        Export shelf as HTML.

        Args:
            shelf_id: Shelf ID

        Returns:
            HTML content
        """
        response = self.client.get(f"shelves/{shelf_id}/export/html")
        return response.get("data", "")

    def export_pdf(self, shelf_id: int) -> bytes:
        """
        Export shelf as PDF.

        Args:
            shelf_id: Shelf ID

        Returns:
            PDF content as bytes
        """
        # Note: This would need special handling for binary content
        # For now, returning the endpoint
        raise NotImplementedError("PDF export requires binary handling")

    def export_markdown(self, shelf_id: int) -> str:
        """
        Export shelf as Markdown.

        Args:
            shelf_id: Shelf ID

        Returns:
            Markdown content
        """
        response = self.client.get(f"shelves/{shelf_id}/export/markdown")
        return response.get("data", "")

    def export_plain_text(self, shelf_id: int) -> str:
        """
        Export shelf as plain text.

        Args:
            shelf_id: Shelf ID

        Returns:
            Plain text content
        """
        response = self.client.get(f"shelves/{shelf_id}/export/plaintext")
        return response.get("data", "")
