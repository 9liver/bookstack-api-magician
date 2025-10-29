"""Books management for BookStack API."""

from typing import List, Dict, Any, Optional


class BooksManager:
    """Manager for BookStack Books operations."""

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
        List all books.

        Args:
            count: Number of items to return
            offset: Offset for pagination
            sort: Sort field (e.g., 'name', '-created_at')
            filter: Filter dictionary

        Returns:
            List of books
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

        response = self.client.get("books", params=params)
        return response.get("data", [])

    def get(self, book_id: int) -> Dict[str, Any]:
        """
        Get a specific book by ID.

        Args:
            book_id: Book ID

        Returns:
            Book data with contents
        """
        response = self.client.get(f"books/{book_id}")
        return response

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new book.

        Args:
            name: Book name
            description: Book description (HTML or Markdown)
            tags: List of tags
            **kwargs: Additional fields

        Returns:
            Created book data
        """
        data = {
            "name": name,
            **kwargs,
        }

        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags

        response = self.client.post("books", json_data=data)
        return response

    def update(
        self,
        book_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Update an existing book.

        Args:
            book_id: Book ID
            name: New book name
            description: New book description
            tags: List of tags
            **kwargs: Additional fields to update

        Returns:
            Updated book data
        """
        data = {**kwargs}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags

        response = self.client.put(f"books/{book_id}", json_data=data)
        return response

    def delete(self, book_id: int) -> bool:
        """
        Delete a book.

        Args:
            book_id: Book ID

        Returns:
            True if successful
        """
        self.client.delete(f"books/{book_id}")
        return True

    def export_html(self, book_id: int) -> str:
        """
        Export book as HTML.

        Args:
            book_id: Book ID

        Returns:
            HTML content
        """
        response = self.client.get(f"books/{book_id}/export/html")
        return response.get("data", "")

    def export_pdf(self, book_id: int) -> bytes:
        """
        Export book as PDF.

        Args:
            book_id: Book ID

        Returns:
            PDF content as bytes
        """
        raise NotImplementedError("PDF export requires binary handling")

    def export_markdown(self, book_id: int) -> str:
        """
        Export book as Markdown.

        Args:
            book_id: Book ID

        Returns:
            Markdown content
        """
        response = self.client.get(f"books/{book_id}/export/markdown")
        return response.get("data", "")

    def export_plain_text(self, book_id: int) -> str:
        """
        Export book as plain text.

        Args:
            book_id: Book ID

        Returns:
            Plain text content
        """
        response = self.client.get(f"books/{book_id}/export/plaintext")
        return response.get("data", "")
