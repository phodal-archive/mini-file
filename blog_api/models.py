"""
Blog API Data Models

This module defines the data models for the blog system including:
- User: Represents a blog user/author
- BlogPost: Represents a blog post with content
- Comment: Represents a comment on a blog post
- Tag: Represents a tag for categorizing posts
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    """User model for blog authors and commenters."""
    id: int = Field(..., description="Unique user identifier")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation timestamp")
    is_active: bool = Field(default=True, description="Whether the user account is active")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True
            }
        }


class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class Tag(BaseModel):
    """Tag model for categorizing blog posts."""
    id: int = Field(..., description="Unique tag identifier")
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")
    slug: str = Field(..., description="URL-friendly tag identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Python",
                "slug": "python"
            }
        }


class TagCreate(BaseModel):
    """Model for creating a new tag."""
    name: str = Field(..., min_length=1, max_length=50)


class Comment(BaseModel):
    """Comment model for blog post comments."""
    id: int = Field(..., description="Unique comment identifier")
    post_id: int = Field(..., description="ID of the blog post this comment belongs to")
    author_id: int = Field(..., description="ID of the comment author")
    content: str = Field(..., min_length=1, max_length=1000, description="Comment content")
    created_at: datetime = Field(default_factory=datetime.now, description="Comment creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "post_id": 1,
                "author_id": 2,
                "content": "Great post! Very informative.",
                "created_at": "2024-01-01T12:00:00"
            }
        }


class CommentCreate(BaseModel):
    """Model for creating a new comment."""
    post_id: int
    author_id: int
    content: str = Field(..., min_length=1, max_length=1000)


class BlogPost(BaseModel):
    """Blog post model with full content and metadata."""
    id: int = Field(..., description="Unique post identifier")
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, description="Post content in markdown")
    author_id: int = Field(..., description="ID of the post author")
    created_at: datetime = Field(default_factory=datetime.now, description="Post creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    published: bool = Field(default=False, description="Whether the post is published")
    tags: List[int] = Field(default_factory=list, description="List of tag IDs")
    view_count: int = Field(default=0, description="Number of times the post has been viewed")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Getting Started with FastAPI",
                "content": "FastAPI is a modern web framework...",
                "author_id": 1,
                "published": True,
                "tags": [1, 2],
                "view_count": 100
            }
        }


class BlogPostCreate(BaseModel):
    """Model for creating a new blog post."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    author_id: int
    published: bool = False
    tags: List[int] = Field(default_factory=list)


class BlogPostUpdate(BaseModel):
    """Model for updating an existing blog post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    published: Optional[bool] = None
    tags: Optional[List[int]] = None


class BlogPostSummary(BaseModel):
    """Summarized blog post for list views."""
    id: int
    title: str
    author_id: int
    created_at: datetime
    published: bool
    tags: List[int]
    view_count: int
    comment_count: int = 0
