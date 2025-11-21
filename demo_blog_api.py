#!/usr/bin/env python3
"""
Blog API Demo Script

This script demonstrates the blog API functionality by:
1. Creating users
2. Creating tags
3. Creating blog posts with tags
4. Adding comments to posts
5. Searching posts
6. Viewing statistics
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_api.services import (
    UserService, TagService, BlogPostService, CommentService, BlogStatisticsService
)
from blog_api.models import (
    UserCreate, TagCreate, BlogPostCreate, CommentCreate, BlogPostUpdate
)
from blog_api.database import db


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo():
    """Run a comprehensive demonstration of the blog API."""
    print("\n" + "🚀" * 30)
    print("       Blog API Demonstration")
    print("🚀" * 30)
    
    # 1. Show initial state (sample data)
    print_section("1. Initial Sample Data")
    users = UserService.get_all_users()
    print(f"Sample users loaded: {len(users)}")
    for user in users:
        print(f"  - {user.username} ({user.email})")
    
    tags = TagService.get_all_tags()
    print(f"\nSample tags loaded: {len(tags)}")
    for tag in tags:
        print(f"  - {tag.name} (slug: {tag.slug})")
    
    # 2. Create a new user
    print_section("2. Creating New User")
    new_user = UserService.create_user(UserCreate(
        username="johndoe",
        email="john@example.com",
        full_name="John Doe"
    ))
    print(f"✓ Created user: {new_user.username}")
    print(f"  ID: {new_user.id}")
    print(f"  Email: {new_user.email}")
    print(f"  Full Name: {new_user.full_name}")
    
    # 3. Create a new tag
    print_section("3. Creating New Tag")
    new_tag = TagService.create_tag(TagCreate(name="Tutorial"))
    print(f"✓ Created tag: {new_tag.name}")
    print(f"  ID: {new_tag.id}")
    print(f"  Slug: {new_tag.slug}")
    
    # 4. Create blog posts
    print_section("4. Creating Blog Posts")
    
    post1 = BlogPostService.create_post(BlogPostCreate(
        title="Getting Started with FastAPI",
        content="""
# Introduction to FastAPI

FastAPI is a modern, fast web framework for building APIs with Python 3.7+.
It's built on top of Starlette and Pydantic, providing excellent performance
and automatic API documentation.

## Key Features
- Fast performance
- Automatic documentation
- Type hints support
- Easy to learn

This is a great framework for building production-ready APIs!
        """.strip(),
        author_id=users[0].id,
        published=True,
        tags=[tags[0].id, tags[1].id, new_tag.id]
    ))
    print(f"✓ Created post 1: '{post1.title}'")
    print(f"  ID: {post1.id}")
    print(f"  Author ID: {post1.author_id}")
    print(f"  Published: {post1.published}")
    print(f"  Tags: {post1.tags}")
    
    post2 = BlogPostService.create_post(BlogPostCreate(
        title="Building RESTful APIs",
        content="""
# REST API Design Best Practices

Learn how to design clean and maintainable REST APIs.

## Best Practices
1. Use proper HTTP methods
2. Return appropriate status codes
3. Version your API
4. Provide clear documentation
5. Handle errors gracefully

Follow these principles to create professional APIs.
        """.strip(),
        author_id=users[1].id,
        published=True,
        tags=[tags[1].id]
    ))
    print(f"\n✓ Created post 2: '{post2.title}'")
    print(f"  ID: {post2.id}")
    print(f"  Author ID: {post2.author_id}")
    
    post3 = BlogPostService.create_post(BlogPostCreate(
        title="Draft: Advanced Python Patterns",
        content="This is a draft post about advanced Python patterns...",
        author_id=new_user.id,
        published=False,
        tags=[tags[0].id]
    ))
    print(f"\n✓ Created post 3: '{post3.title}' (DRAFT)")
    print(f"  ID: {post3.id}")
    
    # 5. View posts
    print_section("5. Viewing All Posts")
    all_posts = BlogPostService.get_posts_summary()
    print(f"Total posts: {len(all_posts)}")
    for post in all_posts:
        status = "📝 Published" if post.published else "📄 Draft"
        print(f"\n{status}: {post.title}")
        print(f"  ID: {post.id} | Views: {post.view_count} | Comments: {post.comment_count}")
    
    # 6. Add comments
    print_section("6. Adding Comments to Posts")
    comment1 = CommentService.create_comment(CommentCreate(
        post_id=post1.id,
        author_id=users[1].id,
        content="Great tutorial! Very helpful for beginners."
    ))
    print(f"✓ Added comment 1 to post '{post1.title}'")
    print(f"  Author ID: {comment1.author_id}")
    print(f"  Content: {comment1.content}")
    
    comment2 = CommentService.create_comment(CommentCreate(
        post_id=post1.id,
        author_id=new_user.id,
        content="Thanks for sharing! Looking forward to more FastAPI content."
    ))
    print(f"\n✓ Added comment 2 to post '{post1.title}'")
    print(f"  Content: {comment2.content}")
    
    comment3 = CommentService.create_comment(CommentCreate(
        post_id=post2.id,
        author_id=users[0].id,
        content="Excellent breakdown of REST principles!"
    ))
    print(f"\n✓ Added comment 3 to post '{post2.title}'")
    print(f"  Content: {comment3.content}")
    
    # 7. Retrieve comments for a post
    print_section("7. Viewing Comments for a Post")
    post1_comments = CommentService.get_comments_for_post(post1.id)
    print(f"Comments on '{post1.title}': {len(post1_comments)}")
    for i, comment in enumerate(post1_comments, 1):
        print(f"\n  Comment {i}:")
        print(f"    Author ID: {comment.author_id}")
        print(f"    Content: {comment.content}")
        print(f"    Posted: {comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 8. Increment view counts
    print_section("8. Simulating Post Views")
    print(f"Initial views for '{post1.title}': {post1.view_count}")
    for i in range(5):
        BlogPostService.get_post(post1.id, increment_views=True)
    updated_post1 = BlogPostService.get_post(post1.id, increment_views=False)
    print(f"After 5 views: {updated_post1.view_count}")
    
    print(f"\nInitial views for '{post2.title}': {post2.view_count}")
    for i in range(3):
        BlogPostService.get_post(post2.id, increment_views=True)
    updated_post2 = BlogPostService.get_post(post2.id, increment_views=False)
    print(f"After 3 views: {updated_post2.view_count}")
    
    # 9. Search posts
    print_section("9. Searching Posts")
    search_query = "FastAPI"
    results = BlogPostService.search_posts(search_query)
    print(f"Search results for '{search_query}': {len(results)} posts found")
    for post in results:
        print(f"  - {post.title} (ID: {post.id})")
    
    search_query2 = "REST"
    results2 = BlogPostService.search_posts(search_query2)
    print(f"\nSearch results for '{search_query2}': {len(results2)} posts found")
    for post in results2:
        print(f"  - {post.title} (ID: {post.id})")
    
    # 10. Get posts by tag
    print_section("10. Getting Posts by Tag")
    python_tag = tags[0]
    posts_with_python = BlogPostService.get_posts_by_tag(python_tag.id)
    print(f"Posts tagged with '{python_tag.name}': {len(posts_with_python)}")
    for post in posts_with_python:
        print(f"  - {post.title}")
    
    # 11. Update a post
    print_section("11. Updating a Post")
    print(f"Original title: {post3.title}")
    print(f"Original published status: {post3.published}")
    
    updated = BlogPostService.update_post(post3.id, BlogPostUpdate(
        title="Advanced Python Patterns (Revised)",
        published=True
    ))
    print(f"\n✓ Updated post")
    print(f"New title: {updated.title}")
    print(f"New published status: {updated.published}")
    print(f"Updated at: {updated.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 12. Statistics
    print_section("12. Blog Statistics")
    stats = {
        "Total Users": BlogStatisticsService.get_total_users(),
        "Total Posts": BlogStatisticsService.get_total_posts(),
        "Published Posts": BlogStatisticsService.get_total_published_posts(),
        "Total Comments": BlogStatisticsService.get_total_comments()
    }
    
    for key, value in stats.items():
        print(f"{key:20s}: {value}")
    
    print("\n📊 Most Viewed Posts:")
    most_viewed = BlogStatisticsService.get_most_viewed_posts(limit=3)
    for i, post in enumerate(most_viewed, 1):
        print(f"  {i}. {post.title} - {post.view_count} views")
    
    print("\n💬 Most Commented Posts:")
    most_commented = BlogStatisticsService.get_most_commented_posts(limit=3)
    for i, post in enumerate(most_commented, 1):
        print(f"  {i}. {post.title} - {post.comment_count} comments")
    
    # 13. Get posts by author
    print_section("13. Getting Posts by Author")
    author = users[0]
    author_posts = BlogPostService.get_posts_by_author(author.id)
    print(f"Posts by user ID {author.id} ({author.username}): {len(author_posts)}")
    for post in author_posts:
        print(f"  - {post.title}")
    
    # 14. Final summary
    print_section("✅ Demo Complete!")
    print("The Blog API successfully demonstrated:")
    print("  ✓ User management")
    print("  ✓ Tag creation and management")
    print("  ✓ Blog post CRUD operations")
    print("  ✓ Comment system")
    print("  ✓ Search functionality")
    print("  ✓ View tracking")
    print("  ✓ Statistics and analytics")
    print("  ✓ Post filtering and querying")
    print("\nThe API is ready for code review! 🎉")
    print("\nTo run the API server:")
    print("  python -m uvicorn blog_api.main:app --reload")
    print("\nThen visit: http://localhost:8000/docs")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    demo()
