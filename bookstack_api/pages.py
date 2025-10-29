"""Pages management for BookStack API."""

from typing import List, Dict, Any, Optional


class PagesManager:
    """Manager for BookStack Pages operations."""

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
        List all pages.

        Args:
            count: Number of items to return
            offset: Offset for pagination
            sort: Sort field
            filter: Filter dictionary

        Returns:
            List of pages
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

        response = self.client.get("pages", params=params)
        return response.get("data", [])

    def get(self, page_id: int) -> Dict[str, Any]:
        """
        Get a specific page by ID.

        Args:
            page_id: Page ID

        Returns:
            Page data with content
        """
        response = self.client.get(f"pages/{page_id}")
        return response

    def create(
        self,
        book_id: int,
        name: str,
        html: Optional[str] = None,
        markdown: Optional[str] = None,
        chapter_id: Optional[int] = None,
        priority: Optional[int] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new page.

        Args:
            book_id: Book ID to create page in
            name: Page name
            html: Page content as HTML
            markdown: Page content as Markdown
            chapter_id: Chapter ID (optional, for pages in chapters)
            priority: Page priority/order
            tags: List of tags
            **kwargs: Additional fields

        Returns:
            Created page data
        """
        data = {
            "book_id": book_id,
            "name": name,
            **kwargs,
        }

        if html is not None:
            data["html"] = html
        if markdown is not None:
            data["markdown"] = markdown
        if chapter_id is not None:
            data["chapter_id"] = chapter_id
        if priority is not None:
            data["priority"] = priority
        if tags is not None:
            data["tags"] = tags

        response = self.client.post("pages", json_data=data)
        return response

    def update(
        self,
        page_id: int,
        name: Optional[str] = None,
        html: Optional[str] = None,
        markdown: Optional[str] = None,
        book_id: Optional[int] = None,
        chapter_id: Optional[int] = None,
        priority: Optional[int] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Update an existing page.

        Args:
            page_id: Page ID
            name: New page name
            html: New HTML content
            markdown: New Markdown content
            book_id: New book ID (to move page)
            chapter_id: New chapter ID (to move page)
            priority: New priority/order
            tags: List of tags
            **kwargs: Additional fields to update

        Returns:
            Updated page data
        """
        data = {**kwargs}

        if name is not None:
            data["name"] = name
        if html is not None:
            data["html"] = html
        if markdown is not None:
            data["markdown"] = markdown
        if book_id is not None:
            data["book_id"] = book_id
        if chapter_id is not None:
            data["chapter_id"] = chapter_id
        if priority is not None:
            data["priority"] = priority
        if tags is not None:
            data["tags"] = tags

        response = self.client.put(f"pages/{page_id}", json_data=data)
        return response

    def delete(self, page_id: int) -> bool:
        """
        Delete a page.

        Args:
            page_id: Page ID

        Returns:
            True if successful
        """
        self.client.delete(f"pages/{page_id}")
        return True

    def export_html(self, page_id: int) -> str:
        """
        Export page as HTML.

        Args:
            page_id: Page ID

        Returns:
            HTML content
        """
        response = self.client.get(f"pages/{page_id}/export/html")
        return response.get("data", "")

    def export_pdf(self, page_id: int) -> bytes:
        """
        Export page as PDF.

        Args:
            page_id: Page ID

        Returns:
            PDF content as bytes
        """
        raise NotImplementedError("PDF export requires binary handling")

    def export_markdown(self, page_id: int) -> str:
        """
        Export page as Markdown.

        Args:
            page_id: Page ID

        Returns:
            Markdown content
        """
        response = self.client.get(f"pages/{page_id}/export/markdown")
        return response.get("data", "")

    def export_plain_text(self, page_id: int) -> str:
        """
        Export page as plain text.

        Args:
            page_id: Page ID

        Returns:
            Plain text content
        """
        response = self.client.get(f"pages/{page_id}/export/plaintext")
        return response.get("data", "")
