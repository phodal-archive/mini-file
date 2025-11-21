"""
Blog API Business Logic Services

This module contains the business logic layer for the blog system.
It orchestrates database operations, applies business rules, and provides
high-level operations for the API endpoints.
"""

from typing import List, Optional

from .database import db
from .models import (
    User, UserCreate, BlogPost, BlogPostCreate, BlogPostUpdate, BlogPostSummary,
    Comment, CommentCreate, Tag, TagCreate
)


class UserService:
    """Service for user-related business logic."""
    
    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        """
        Create a new user with validation.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user object
            
        Raises:
            ValueError: If username already exists
        """
        # Check if username already exists
        existing = db.get_user_by_username(user_data.username)
        if existing:
            raise ValueError(f"Username '{user_data.username}' already exists")
        
        user_dict = db.create_user(user_data.model_dump())
        return User(**user_dict)
    
    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        """Get a user by ID."""
        user_dict = db.get_user(user_id)
        return User(**user_dict) if user_dict else None
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Get all users."""
        return [User(**user_dict) for user_dict in db.get_all_users()]
    
    @staticmethod
    def user_exists(user_id: int) -> bool:
        """Check if a user exists."""
        return db.get_user(user_id) is not None


class TagService:
    """Service for tag-related business logic."""
    
    @staticmethod
    def create_tag(tag_data: TagCreate) -> Tag:
        """
        Create a new tag.
        
        Args:
            tag_data: Tag creation data
            
        Returns:
            Created tag object
        """
        tag_dict = db.create_tag(tag_data.model_dump())
        return Tag(**tag_dict)
    
    @staticmethod
    def get_tag(tag_id: int) -> Optional[Tag]:
        """Get a tag by ID."""
        tag_dict = db.get_tag(tag_id)
        return Tag(**tag_dict) if tag_dict else None
    
    @staticmethod
    def get_all_tags() -> List[Tag]:
        """Get all tags."""
        return [Tag(**tag_dict) for tag_dict in db.get_all_tags()]
    
    @staticmethod
    def validate_tag_ids(tag_ids: List[int]) -> bool:
        """Validate that all tag IDs exist."""
        for tag_id in tag_ids:
            if not db.get_tag(tag_id):
                return False
        return True


class BlogPostService:
    """Service for blog post-related business logic."""
    
    @staticmethod
    def create_post(post_data: BlogPostCreate) -> BlogPost:
        """
        Create a new blog post with validation.
        
        Args:
            post_data: Post creation data
            
        Returns:
            Created blog post object
            
        Raises:
            ValueError: If author doesn't exist or tags are invalid
        """
        # Validate author exists
        if not UserService.user_exists(post_data.author_id):
            raise ValueError(f"Author with ID {post_data.author_id} does not exist")
        
        # Validate tags if provided
        if post_data.tags and not TagService.validate_tag_ids(post_data.tags):
            raise ValueError("One or more tag IDs are invalid")
        
        post_dict = db.create_post(post_data.model_dump())
        return BlogPost(**post_dict)
    
    @staticmethod
    def get_post(post_id: int, increment_views: bool = False) -> Optional[BlogPost]:
        """
        Get a blog post by ID.
        
        Args:
            post_id: ID of the post to retrieve
            increment_views: Whether to increment the view count
            
        Returns:
            Blog post object or None if not found
        """
        if increment_views:
            db.increment_view_count(post_id)
        
        post_dict = db.get_post(post_id)
        return BlogPost(**post_dict) if post_dict else None
    
    @staticmethod
    def update_post(post_id: int, update_data: BlogPostUpdate) -> Optional[BlogPost]:
        """
        Update a blog post.
        
        Args:
            post_id: ID of the post to update
            update_data: Data to update
            
        Returns:
            Updated blog post or None if not found
            
        Raises:
            ValueError: If tags are invalid
        """
        # Validate tags if provided in update
        if update_data.tags is not None and not TagService.validate_tag_ids(update_data.tags):
            raise ValueError("One or more tag IDs are invalid")
        
        # Filter out None values for partial updates
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        
        post_dict = db.update_post(post_id, update_dict)
        return BlogPost(**post_dict) if post_dict else None
    
    @staticmethod
    def delete_post(post_id: int) -> bool:
        """Delete a blog post."""
        return db.delete_post(post_id)
    
    @staticmethod
    def get_all_posts(published_only: bool = False) -> List[BlogPost]:
        """Get all blog posts."""
        return [BlogPost(**post_dict) for post_dict in db.get_all_posts(published_only)]
    
    @staticmethod
    def get_posts_summary(published_only: bool = False) -> List[BlogPostSummary]:
        """
        Get summarized list of blog posts with comment counts.
        
        Args:
            published_only: Whether to return only published posts
            
        Returns:
            List of blog post summaries
        """
        posts = db.get_all_posts(published_only)
        summaries = []
        
        for post_dict in posts:
            comment_count = db.get_comment_count_for_post(post_dict["id"])
            summary = BlogPostSummary(
                **post_dict,
                comment_count=comment_count
            )
            summaries.append(summary)
        
        return summaries
    
    @staticmethod
    def get_posts_by_author(author_id: int) -> List[BlogPost]:
        """Get all posts by a specific author."""
        return [BlogPost(**post_dict) for post_dict in db.get_posts_by_author(author_id)]
    
    @staticmethod
    def get_posts_by_tag(tag_id: int) -> List[BlogPost]:
        """Get all posts with a specific tag."""
        return [BlogPost(**post_dict) for post_dict in db.get_posts_by_tag(tag_id)]
    
    @staticmethod
    def search_posts(query: str) -> List[BlogPost]:
        """Search posts by title or content."""
        return [BlogPost(**post_dict) for post_dict in db.search_posts(query)]
    
    @staticmethod
    def publish_post(post_id: int) -> Optional[BlogPost]:
        """Publish a blog post."""
        return BlogPostService.update_post(post_id, BlogPostUpdate(published=True))
    
    @staticmethod
    def unpublish_post(post_id: int) -> Optional[BlogPost]:
        """Unpublish a blog post."""
        return BlogPostService.update_post(post_id, BlogPostUpdate(published=False))


class CommentService:
    """Service for comment-related business logic."""
    
    @staticmethod
    def create_comment(comment_data: CommentCreate) -> Comment:
        """
        Create a new comment with validation.
        
        Args:
            comment_data: Comment creation data
            
        Returns:
            Created comment object
            
        Raises:
            ValueError: If post or author doesn't exist
        """
        # Validate post exists
        if not db.get_post(comment_data.post_id):
            raise ValueError(f"Post with ID {comment_data.post_id} does not exist")
        
        # Validate author exists
        if not UserService.user_exists(comment_data.author_id):
            raise ValueError(f"Author with ID {comment_data.author_id} does not exist")
        
        comment_dict = db.create_comment(comment_data.model_dump())
        return Comment(**comment_dict)
    
    @staticmethod
    def get_comment(comment_id: int) -> Optional[Comment]:
        """Get a comment by ID."""
        comment_dict = db.get_comment(comment_id)
        return Comment(**comment_dict) if comment_dict else None
    
    @staticmethod
    def get_comments_for_post(post_id: int) -> List[Comment]:
        """Get all comments for a specific post."""
        return [Comment(**c_dict) for c_dict in db.get_comments_for_post(post_id)]
    
    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """Delete a comment."""
        return db.delete_comment(comment_id)


class BlogStatisticsService:
    """Service for blog statistics and analytics."""
    
    @staticmethod
    def get_total_posts() -> int:
        """Get total number of posts."""
        return len(db.posts)
    
    @staticmethod
    def get_total_published_posts() -> int:
        """Get total number of published posts."""
        return len(db.get_all_posts(published_only=True))
    
    @staticmethod
    def get_total_comments() -> int:
        """Get total number of comments."""
        return len(db.comments)
    
    @staticmethod
    def get_total_users() -> int:
        """Get total number of users."""
        return len(db.users)
    
    @staticmethod
    def get_most_viewed_posts(limit: int = 5) -> List[BlogPost]:
        """Get the most viewed posts."""
        posts = db.get_all_posts()
        sorted_posts = sorted(posts, key=lambda x: x["view_count"], reverse=True)
        return [BlogPost(**post_dict) for post_dict in sorted_posts[:limit]]
    
    @staticmethod
    def get_most_commented_posts(limit: int = 5) -> List[BlogPostSummary]:
        """Get the most commented posts."""
        summaries = BlogPostService.get_posts_summary()
        sorted_summaries = sorted(summaries, key=lambda x: x.comment_count, reverse=True)
        return sorted_summaries[:limit]
