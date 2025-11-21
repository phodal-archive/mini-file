#!/usr/bin/env python3
"""
Tests for Blog API

Simple tests to validate the blog API functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from blog_api.services import (
    UserService, TagService, BlogPostService, CommentService, BlogStatisticsService
)
from blog_api.models import UserCreate, TagCreate, BlogPostCreate, CommentCreate, BlogPostUpdate
from blog_api.database import db


def reset_database():
    """Reset database to initial state."""
    db.users.clear()
    db.posts.clear()
    db.comments.clear()
    db.tags.clear()
    db.user_counter = 0
    db.post_counter = 0
    db.comment_counter = 0
    db.tag_counter = 0
    db._init_sample_data()


def test_user_creation():
    """Test creating a new user."""
    reset_database()
    
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User"
    )
    
    user = UserService.create_user(user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    
    print("✓ test_user_creation passed")


def test_duplicate_username():
    """Test that duplicate usernames are rejected."""
    reset_database()
    
    user_data = UserCreate(username="admin", email="test@example.com")
    
    try:
        UserService.create_user(user_data)
        assert False, "Should have raised ValueError for duplicate username"
    except ValueError as e:
        assert "already exists" in str(e)
    
    print("✓ test_duplicate_username passed")


def test_tag_creation():
    """Test creating a new tag."""
    reset_database()
    
    tag_data = TagCreate(name="JavaScript")
    tag = TagService.create_tag(tag_data)
    
    assert tag.name == "JavaScript"
    assert tag.slug == "javascript"
    
    print("✓ test_tag_creation passed")


def test_blog_post_creation():
    """Test creating a blog post."""
    reset_database()
    
    # Get an existing user
    users = UserService.get_all_users()
    author_id = users[0].id
    
    # Get existing tags
    tags = TagService.get_all_tags()
    tag_ids = [tags[0].id] if tags else []
    
    post_data = BlogPostCreate(
        title="Test Post",
        content="This is test content",
        author_id=author_id,
        published=True,
        tags=tag_ids
    )
    
    post = BlogPostService.create_post(post_data)
    
    assert post.title == "Test Post"
    assert post.content == "This is test content"
    assert post.author_id == author_id
    assert post.published is True
    assert post.view_count == 0
    
    print("✓ test_blog_post_creation passed")


def test_blog_post_with_invalid_author():
    """Test that creating a post with invalid author fails."""
    reset_database()
    
    post_data = BlogPostCreate(
        title="Test",
        content="Content",
        author_id=9999,  # Non-existent author
        published=False
    )
    
    try:
        BlogPostService.create_post(post_data)
        assert False, "Should have raised ValueError for invalid author"
    except ValueError as e:
        assert "does not exist" in str(e)
    
    print("✓ test_blog_post_with_invalid_author passed")


def test_blog_post_update():
    """Test updating a blog post."""
    reset_database()
    
    # Create a post first
    users = UserService.get_all_users()
    post_data = BlogPostCreate(
        title="Original Title",
        content="Original Content",
        author_id=users[0].id,
        published=False
    )
    post = BlogPostService.create_post(post_data)
    
    # Update the post
    update_data = BlogPostUpdate(
        title="Updated Title",
        published=True
    )
    updated_post = BlogPostService.update_post(post.id, update_data)
    
    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Original Content"  # Unchanged
    assert updated_post.published is True
    assert updated_post.updated_at is not None
    
    print("✓ test_blog_post_update passed")


def test_comment_creation():
    """Test creating a comment on a post."""
    reset_database()
    
    # Create a post and users
    users = UserService.get_all_users()
    author_id = users[0].id
    
    post_data = BlogPostCreate(
        title="Post with comments",
        content="Content here",
        author_id=author_id,
        published=True
    )
    post = BlogPostService.create_post(post_data)
    
    # Create a comment
    commenter_id = users[1].id if len(users) > 1 else author_id
    comment_data = CommentCreate(
        post_id=post.id,
        author_id=commenter_id,
        content="Great post!"
    )
    
    comment = CommentService.create_comment(comment_data)
    
    assert comment.post_id == post.id
    assert comment.author_id == commenter_id
    assert comment.content == "Great post!"
    
    print("✓ test_comment_creation passed")


def test_get_post_comments():
    """Test retrieving comments for a post."""
    reset_database()
    
    # Create post and comments
    users = UserService.get_all_users()
    author_id = users[0].id
    
    post_data = BlogPostCreate(
        title="Test Post",
        content="Content",
        author_id=author_id
    )
    post = BlogPostService.create_post(post_data)
    
    # Add multiple comments
    for i in range(3):
        comment_data = CommentCreate(
            post_id=post.id,
            author_id=author_id,
            content=f"Comment {i+1}"
        )
        CommentService.create_comment(comment_data)
    
    # Retrieve comments
    comments = CommentService.get_comments_for_post(post.id)
    
    assert len(comments) == 3
    assert comments[0].content == "Comment 1"
    
    print("✓ test_get_post_comments passed")


def test_view_count_increment():
    """Test that view count increments correctly."""
    reset_database()
    
    users = UserService.get_all_users()
    post_data = BlogPostCreate(
        title="Popular Post",
        content="This will be viewed many times",
        author_id=users[0].id
    )
    post = BlogPostService.create_post(post_data)
    
    initial_views = post.view_count
    assert initial_views == 0
    
    # Get post with view increment
    BlogPostService.get_post(post.id, increment_views=True)
    BlogPostService.get_post(post.id, increment_views=True)
    BlogPostService.get_post(post.id, increment_views=True)
    
    # Check updated view count
    updated_post = BlogPostService.get_post(post.id, increment_views=False)
    assert updated_post.view_count == 3
    
    print("✓ test_view_count_increment passed")


def test_search_posts():
    """Test searching posts by content."""
    reset_database()
    
    users = UserService.get_all_users()
    author_id = users[0].id
    
    # Create posts with different content
    BlogPostService.create_post(BlogPostCreate(
        title="Python Tutorial",
        content="Learn Python programming",
        author_id=author_id
    ))
    
    BlogPostService.create_post(BlogPostCreate(
        title="JavaScript Guide",
        content="Learn JavaScript basics",
        author_id=author_id
    ))
    
    # Search for Python
    results = BlogPostService.search_posts("Python")
    assert len(results) == 1
    assert "Python" in results[0].title
    
    print("✓ test_search_posts passed")


def test_statistics():
    """Test statistics service."""
    reset_database()
    
    stats_total_users = BlogStatisticsService.get_total_users()
    assert stats_total_users > 0
    
    stats_total_posts = BlogStatisticsService.get_total_posts()
    assert stats_total_posts >= 0
    
    print("✓ test_statistics passed")


def test_delete_post_cascade():
    """Test that deleting a post also deletes its comments."""
    reset_database()
    
    users = UserService.get_all_users()
    author_id = users[0].id
    
    # Create post
    post = BlogPostService.create_post(BlogPostCreate(
        title="Post to delete",
        content="This will be deleted",
        author_id=author_id
    ))
    
    # Add comment
    CommentService.create_comment(CommentCreate(
        post_id=post.id,
        author_id=author_id,
        content="This comment will also be deleted"
    ))
    
    # Verify comment exists
    comments_before = CommentService.get_comments_for_post(post.id)
    assert len(comments_before) == 1
    
    # Delete post
    BlogPostService.delete_post(post.id)
    
    # Verify post is gone
    deleted_post = BlogPostService.get_post(post.id)
    assert deleted_post is None
    
    # Verify comments are gone
    comments_after = CommentService.get_comments_for_post(post.id)
    assert len(comments_after) == 0
    
    print("✓ test_delete_post_cascade passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Blog API Tests")
    print("=" * 50)
    print()
    
    tests = [
        test_user_creation,
        test_duplicate_username,
        test_tag_creation,
        test_blog_post_creation,
        test_blog_post_with_invalid_author,
        test_blog_post_update,
        test_comment_creation,
        test_get_post_comments,
        test_view_count_increment,
        test_search_posts,
        test_statistics,
        test_delete_post_cascade,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    total = len(tests)
    passed = total - failed
    print(f"Tests: {passed}/{total} passed")
    if failed == 0:
        print("All tests passed! ✓")
    else:
        print(f"{failed} test(s) failed ✗")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
