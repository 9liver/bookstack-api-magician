"""Data models for BookStack API resources."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BookStackModel(BaseModel):
    """Base model for all BookStack resources."""
    model_config = ConfigDict(extra='allow')

    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Shelf(BookStackModel):
    """Represents a BookStack Shelf."""
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    owned_by: Optional[int] = None
    books: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[Dict[str, Any]]] = None


class Book(BookStackModel):
    """Represents a BookStack Book."""
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    owned_by: Optional[int] = None
    cover: Optional[Dict[str, Any]] = None
    tags: Optional[List[Dict[str, Any]]] = None


class Chapter(BookStackModel):
    """Represents a BookStack Chapter."""
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    book_id: int
    priority: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    owned_by: Optional[int] = None
    tags: Optional[List[Dict[str, Any]]] = None


class Page(BookStackModel):
    """Represents a BookStack Page."""
    name: str
    slug: Optional[str] = None
    book_id: int
    chapter_id: Optional[int] = None
    html: Optional[str] = None
    markdown: Optional[str] = None
    priority: Optional[int] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    owned_by: Optional[int] = None
    draft: Optional[bool] = False
    revision_count: Optional[int] = None
    template: Optional[bool] = False
    tags: Optional[List[Dict[str, Any]]] = None


class User(BookStackModel):
    """Represents a BookStack User."""
    name: str
    email: str
    slug: Optional[str] = None
    external_auth_id: Optional[str] = None
    language: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = None
    avatar: Optional[Dict[str, Any]] = None
    password: Optional[str] = None
    send_invite: Optional[bool] = None


class Role(BookStackModel):
    """Represents a BookStack Role."""
    display_name: str
    description: Optional[str] = None
    external_auth_id: Optional[str] = None
    mfa_enforced: Optional[bool] = False


class Tag(BaseModel):
    """Represents a BookStack Tag."""
    name: str
    value: Optional[str] = None
    order: Optional[int] = None
