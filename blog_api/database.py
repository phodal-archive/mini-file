"""
Blog API Database Layer

This module provides in-memory database operations for the blog system.
It simulates a real database with thread-safe operations and includes:
- User management
- Blog post CRUD operations
- Comment management
- Tag management
- Search and filtering capabilities
"""

from datetime import datetime
from typing import List, Optional, Dict
from threading import Lock
import re


class BlogDatabase:
    """In-memory database for blog data with thread-safe operations."""
    
    def __init__(self):
        """Initialize the database with empty collections."""
        self.users: Dict[int, dict] = {}
        self.posts: Dict[int, dict] = {}
        self.comments: Dict[int, dict] = {}
        self.tags: Dict[int, dict] = {}
        
        # Auto-increment counters
        self.user_counter = 0
        self.post_counter = 0
        self.comment_counter = 0
        self.tag_counter = 0
        
        # Thread safety locks
        self.user_lock = Lock()
        self.post_lock = Lock()
        self.comment_lock = Lock()
        self.tag_lock = Lock()
        
        # Initialize with some sample data
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize database with sample data for demonstration."""
        # Create sample users
        self.create_user({
            "username": "admin",
            "email": "admin@blog.com",
            "full_name": "Admin User"
        })
        
        self.create_user({
            "username": "alice",
            "email": "alice@example.com",
            "full_name": "Alice Johnson"
        })
        
        # Create sample tags
        self.create_tag({"name": "Python"})
        self.create_tag({"name": "FastAPI"})
        self.create_tag({"name": "Web Development"})
    
    # User operations
    def create_user(self, user_data: dict) -> dict:
        """Create a new user and return the created user."""
        with self.user_lock:
            self.user_counter += 1
            user = {
                "id": self.user_counter,
                "username": user_data["username"],
                "email": user_data["email"],
                "full_name": user_data.get("full_name"),
                "created_at": datetime.now(),
                "is_active": True
            }
            self.users[user["id"]] = user
            return user.copy()
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get a user by ID."""
        return self.users.get(user_id, {}).copy() if user_id in self.users else None
    
    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Get a user by username."""
        for user in self.users.values():
            if user["username"] == username:
                return user.copy()
        return None
    
    def get_all_users(self) -> List[dict]:
        """Get all users."""
        return [user.copy() for user in self.users.values()]
    
    # Tag operations
    def create_tag(self, tag_data: dict) -> dict:
        """Create a new tag and return the created tag."""
        with self.tag_lock:
            self.tag_counter += 1
            slug = self._slugify(tag_data["name"])
            tag = {
                "id": self.tag_counter,
                "name": tag_data["name"],
                "slug": slug
            }
            self.tags[tag["id"]] = tag
            return tag.copy()
    
    def get_tag(self, tag_id: int) -> Optional[dict]:
        """Get a tag by ID."""
        return self.tags.get(tag_id, {}).copy() if tag_id in self.tags else None
    
    def get_all_tags(self) -> List[dict]:
        """Get all tags."""
        return [tag.copy() for tag in self.tags.values()]
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    # Post operations
    def create_post(self, post_data: dict) -> dict:
        """Create a new blog post and return the created post."""
        with self.post_lock:
            self.post_counter += 1
            post = {
                "id": self.post_counter,
                "title": post_data["title"],
                "content": post_data["content"],
                "author_id": post_data["author_id"],
                "created_at": datetime.now(),
                "updated_at": None,
                "published": post_data.get("published", False),
                "tags": post_data.get("tags", []),
                "view_count": 0
            }
            self.posts[post["id"]] = post
            return post.copy()
    
    def get_post(self, post_id: int) -> Optional[dict]:
        """Get a blog post by ID."""
        return self.posts.get(post_id, {}).copy() if post_id in self.posts else None
    
    def update_post(self, post_id: int, update_data: dict) -> Optional[dict]:
        """Update a blog post and return the updated post."""
        with self.post_lock:
            if post_id not in self.posts:
                return None
            
            post = self.posts[post_id]
            for key, value in update_data.items():
                if value is not None and key != "id":
                    post[key] = value
            
            post["updated_at"] = datetime.now()
            return post.copy()
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a blog post. Returns True if successful."""
        with self.post_lock:
            if post_id in self.posts:
                del self.posts[post_id]
                # Also delete associated comments
                self._delete_comments_for_post(post_id)
                return True
            return False
    
    def get_all_posts(self, published_only: bool = False) -> List[dict]:
        """Get all blog posts, optionally filtered by published status."""
        posts = [post.copy() for post in self.posts.values()]
        if published_only:
            posts = [post for post in posts if post["published"]]
        return sorted(posts, key=lambda x: x["created_at"], reverse=True)
    
    def get_posts_by_author(self, author_id: int) -> List[dict]:
        """Get all posts by a specific author."""
        return [post.copy() for post in self.posts.values() if post["author_id"] == author_id]
    
    def get_posts_by_tag(self, tag_id: int) -> List[dict]:
        """Get all posts with a specific tag."""
        return [post.copy() for post in self.posts.values() if tag_id in post.get("tags", [])]
    
    def increment_view_count(self, post_id: int) -> bool:
        """Increment the view count for a post."""
        with self.post_lock:
            if post_id in self.posts:
                self.posts[post_id]["view_count"] += 1
                return True
            return False
    
    def search_posts(self, query: str) -> List[dict]:
        """Search posts by title or content."""
        query_lower = query.lower()
        results = []
        for post in self.posts.values():
            if (query_lower in post["title"].lower() or 
                query_lower in post["content"].lower()):
                results.append(post.copy())
        return sorted(results, key=lambda x: x["created_at"], reverse=True)
    
    # Comment operations
    def create_comment(self, comment_data: dict) -> dict:
        """Create a new comment and return the created comment."""
        with self.comment_lock:
            self.comment_counter += 1
            comment = {
                "id": self.comment_counter,
                "post_id": comment_data["post_id"],
                "author_id": comment_data["author_id"],
                "content": comment_data["content"],
                "created_at": datetime.now(),
                "updated_at": None
            }
            self.comments[comment["id"]] = comment
            return comment.copy()
    
    def get_comment(self, comment_id: int) -> Optional[dict]:
        """Get a comment by ID."""
        return self.comments.get(comment_id, {}).copy() if comment_id in self.comments else None
    
    def get_comments_for_post(self, post_id: int) -> List[dict]:
        """Get all comments for a specific post."""
        comments = [c.copy() for c in self.comments.values() if c["post_id"] == post_id]
        return sorted(comments, key=lambda x: x["created_at"])
    
    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment. Returns True if successful."""
        with self.comment_lock:
            if comment_id in self.comments:
                del self.comments[comment_id]
                return True
            return False
    
    def _delete_comments_for_post(self, post_id: int):
        """Delete all comments associated with a post (internal method)."""
        with self.comment_lock:
            comment_ids_to_delete = [
                cid for cid, comment in self.comments.items() 
                if comment["post_id"] == post_id
            ]
            for cid in comment_ids_to_delete:
                del self.comments[cid]
    
    def get_comment_count_for_post(self, post_id: int) -> int:
        """Get the number of comments for a specific post."""
        return sum(1 for c in self.comments.values() if c["post_id"] == post_id)


# Global database instance
db = BlogDatabase()
