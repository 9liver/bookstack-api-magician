"""Chapters management for BookStack API."""

from typing import List, Dict, Any, Optional


class ChaptersManager:
    """Manager for BookStack Chapters operations."""

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
        List all chapters.

        Args:
            count: Number of items to return
            offset: Offset for pagination
            sort: Sort field
            filter: Filter dictionary

        Returns:
            List of chapters
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

        response = self.client.get("chapters", params=params)
        return response.get("data", [])

    def get(self, chapter_id: int) -> Dict[str, Any]:
        """
        Get a specific chapter by ID.

        Args:
            chapter_id: Chapter ID

        Returns:
            Chapter data
        """
        response = self.client.get(f"chapters/{chapter_id}")
        return response

    def create(
        self,
        book_id: int,
        name: str,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new chapter.

        Args:
            book_id: Book ID to create chapter in
            name: Chapter name
            description: Chapter description
            priority: Chapter priority/order
            tags: List of tags
            **kwargs: Additional fields

        Returns:
            Created chapter data
        """
        data = {
            "book_id": book_id,
            "name": name,
            **kwargs,
        }

        if description is not None:
            data["description"] = description
        if priority is not None:
            data["priority"] = priority
        if tags is not None:
            data["tags"] = tags

        response = self.client.post("chapters", json_data=data)
        return response

    def update(
        self,
        chapter_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        book_id: Optional[int] = None,
        priority: Optional[int] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Update an existing chapter.

        Args:
            chapter_id: Chapter ID
            name: New chapter name
            description: New chapter description
            book_id: New book ID (to move chapter)
            priority: New priority/order
            tags: List of tags
            **kwargs: Additional fields to update

        Returns:
            Updated chapter data
        """
        data = {**kwargs}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if book_id is not None:
            data["book_id"] = book_id
        if priority is not None:
            data["priority"] = priority
        if tags is not None:
            data["tags"] = tags

        response = self.client.put(f"chapters/{chapter_id}", json_data=data)
        return response

    def delete(self, chapter_id: int) -> bool:
        """
        Delete a chapter.

        Args:
            chapter_id: Chapter ID

        Returns:
            True if successful
        """
        self.client.delete(f"chapters/{chapter_id}")
        return True

    def export_html(self, chapter_id: int) -> str:
        """
        Export chapter as HTML.

        Args:
            chapter_id: Chapter ID

        Returns:
            HTML content
        """
        response = self.client.get(f"chapters/{chapter_id}/export/html")
        return response.get("data", "")

    def export_pdf(self, chapter_id: int) -> bytes:
        """
        Export chapter as PDF.

        Args:
            chapter_id: Chapter ID

        Returns:
            PDF content as bytes
        """
        raise NotImplementedError("PDF export requires binary handling")

    def export_markdown(self, chapter_id: int) -> str:
        """
        Export chapter as Markdown.

        Args:
            chapter_id: Chapter ID

        Returns:
            Markdown content
        """
        response = self.client.get(f"chapters/{chapter_id}/export/markdown")
        return response.get("data", "")

    def export_plain_text(self, chapter_id: int) -> str:
        """
        Export chapter as plain text.

        Args:
            chapter_id: Chapter ID

        Returns:
            Plain text content
        """
        response = self.client.get(f"chapters/{chapter_id}/export/plaintext")
        return response.get("data", "")
