"""
FastAPI Blog API

A comprehensive blog API built with FastAPI demonstrating:
- RESTful API design
- Complex business logic with multiple interacting services
- CRUD operations for blog posts, comments, users, and tags
- Search and filtering capabilities
- Statistics and analytics endpoints

This serves as a demonstration for code review agents to analyze
complex multi-file Python applications with various architectural patterns.
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import List, Optional

from .models import (
    User, UserCreate, BlogPost, BlogPostCreate, BlogPostUpdate, BlogPostSummary,
    Comment, CommentCreate, Tag, TagCreate
)
from .services import (
    UserService, TagService, BlogPostService, CommentService, BlogStatisticsService
)


# Initialize FastAPI app
app = FastAPI(
    title="Blog API",
    description="A comprehensive blog API with posts, comments, users, and tags",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with API information."""
    return {
        "message": "Welcome to the Blog API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "users": "/users",
            "posts": "/posts",
            "comments": "/comments",
            "tags": "/tags",
            "statistics": "/statistics"
        }
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "blog-api"}


# ===========================
# User Endpoints
# ===========================

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """Create a new user."""
    try:
        return UserService.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/users", response_model=List[User], tags=["Users"])
async def get_users():
    """Get all users."""
    return UserService.get_all_users()


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """Get a specific user by ID."""
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.get("/users/{user_id}/posts", response_model=List[BlogPost], tags=["Users"])
async def get_user_posts(user_id: int):
    """Get all posts by a specific user."""
    if not UserService.user_exists(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return BlogPostService.get_posts_by_author(user_id)


# ===========================
# Tag Endpoints
# ===========================

@app.post("/tags", response_model=Tag, status_code=status.HTTP_201_CREATED, tags=["Tags"])
async def create_tag(tag: TagCreate):
    """Create a new tag."""
    return TagService.create_tag(tag)


@app.get("/tags", response_model=List[Tag], tags=["Tags"])
async def get_tags():
    """Get all tags."""
    return TagService.get_all_tags()


@app.get("/tags/{tag_id}", response_model=Tag, tags=["Tags"])
async def get_tag(tag_id: int):
    """Get a specific tag by ID."""
    tag = TagService.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@app.get("/tags/{tag_id}/posts", response_model=List[BlogPost], tags=["Tags"])
async def get_posts_by_tag(tag_id: int):
    """Get all posts with a specific tag."""
    tag = TagService.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return BlogPostService.get_posts_by_tag(tag_id)


# ===========================
# Blog Post Endpoints
# ===========================

@app.post("/posts", response_model=BlogPost, status_code=status.HTTP_201_CREATED, tags=["Posts"])
async def create_post(post: BlogPostCreate):
    """Create a new blog post."""
    try:
        return BlogPostService.create_post(post)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/posts", response_model=List[BlogPostSummary], tags=["Posts"])
async def get_posts(
    published_only: bool = Query(False, description="Filter to show only published posts")
):
    """Get all blog posts with summaries."""
    return BlogPostService.get_posts_summary(published_only=published_only)


@app.get("/posts/{post_id}", response_model=BlogPost, tags=["Posts"])
async def get_post(
    post_id: int,
    increment_views: bool = Query(True, description="Increment view count")
):
    """Get a specific blog post by ID."""
    post = BlogPostService.get_post(post_id, increment_views=increment_views)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@app.put("/posts/{post_id}", response_model=BlogPost, tags=["Posts"])
async def update_post(post_id: int, update_data: BlogPostUpdate):
    """Update a blog post."""
    try:
        post = BlogPostService.update_post(post_id, update_data)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
async def delete_post(post_id: int):
    """Delete a blog post."""
    if not BlogPostService.delete_post(post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return None


@app.post("/posts/{post_id}/publish", response_model=BlogPost, tags=["Posts"])
async def publish_post(post_id: int):
    """Publish a blog post."""
    post = BlogPostService.publish_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@app.post("/posts/{post_id}/unpublish", response_model=BlogPost, tags=["Posts"])
async def unpublish_post(post_id: int):
    """Unpublish a blog post."""
    post = BlogPostService.unpublish_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


# ===========================
# Comment Endpoints
# ===========================

@app.post("/comments", response_model=Comment, status_code=status.HTTP_201_CREATED, tags=["Comments"])
async def create_comment(comment: CommentCreate):
    """Create a new comment on a blog post."""
    try:
        return CommentService.create_comment(comment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/comments/{comment_id}", response_model=Comment, tags=["Comments"])
async def get_comment(comment_id: int):
    """Get a specific comment by ID."""
    comment = CommentService.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@app.get("/posts/{post_id}/comments", response_model=List[Comment], tags=["Comments"])
async def get_post_comments(post_id: int):
    """Get all comments for a specific post."""
    # Verify post exists
    post = BlogPostService.get_post(post_id, increment_views=False)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return CommentService.get_comments_for_post(post_id)


@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comments"])
async def delete_comment(comment_id: int):
    """Delete a comment."""
    if not CommentService.delete_comment(comment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return None


# ===========================
# Search Endpoints
# ===========================

@app.get("/search", response_model=List[BlogPost], tags=["Search"])
async def search_posts(
    q: str = Query(..., min_length=1, description="Search query")
):
    """Search blog posts by title or content."""
    return BlogPostService.search_posts(q)


# ===========================
# Statistics Endpoints
# ===========================

@app.get("/statistics", tags=["Statistics"])
async def get_statistics():
    """Get overall blog statistics."""
    return {
        "total_posts": BlogStatisticsService.get_total_posts(),
        "total_published_posts": BlogStatisticsService.get_total_published_posts(),
        "total_comments": BlogStatisticsService.get_total_comments(),
        "total_users": BlogStatisticsService.get_total_users()
    }


@app.get("/statistics/most-viewed", response_model=List[BlogPost], tags=["Statistics"])
async def get_most_viewed_posts(
    limit: int = Query(5, ge=1, le=20, description="Number of posts to return")
):
    """Get the most viewed blog posts."""
    return BlogStatisticsService.get_most_viewed_posts(limit)


@app.get("/statistics/most-commented", response_model=List[BlogPostSummary], tags=["Statistics"])
async def get_most_commented_posts(
    limit: int = Query(5, ge=1, le=20, description="Number of posts to return")
):
    """Get the most commented blog posts."""
    return BlogStatisticsService.get_most_commented_posts(limit)


# ===========================
# Error Handlers
# ===========================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    print("Starting Blog API server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
