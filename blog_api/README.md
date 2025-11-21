# Blog API - FastAPI Example

A comprehensive blog API built with FastAPI demonstrating complex multi-file architecture, RESTful design, and business logic separation.

## 🏗️ Architecture

This project demonstrates a well-structured FastAPI application with clear separation of concerns:

- **models.py**: Pydantic data models and schemas
- **database.py**: In-memory database with thread-safe operations
- **services.py**: Business logic layer
- **main.py**: FastAPI application with REST endpoints

## 📊 System Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Client[HTTP Client/Browser]
    end
    
    subgraph "API Layer - main.py"
        API[FastAPI Routes]
        ErrorHandler[Error Handlers]
    end
    
    subgraph "Service Layer - services.py"
        UserService[User Service]
        PostService[Blog Post Service]
        CommentService[Comment Service]
        TagService[Tag Service]
        StatsService[Statistics Service]
    end
    
    subgraph "Data Layer - database.py"
        DB[(In-Memory Database)]
        UserTable[Users]
        PostTable[Posts]
        CommentTable[Comments]
        TagTable[Tags]
    end
    
    subgraph "Model Layer - models.py"
        Models[Pydantic Models]
        Validation[Data Validation]
    end
    
    Client -->|HTTP Request| API
    API -->|Business Logic| UserService
    API -->|Business Logic| PostService
    API -->|Business Logic| CommentService
    API -->|Business Logic| TagService
    API -->|Business Logic| StatsService
    
    UserService -->|CRUD Operations| DB
    PostService -->|CRUD Operations| DB
    CommentService -->|CRUD Operations| DB
    TagService -->|CRUD Operations| DB
    StatsService -->|Analytics| DB
    
    DB --> UserTable
    DB --> PostTable
    DB --> CommentTable
    DB --> TagTable
    
    API -.->|Validates with| Models
    UserService -.->|Uses| Models
    PostService -.->|Uses| Models
    CommentService -.->|Uses| Models
    TagService -.->|Uses| Models
```

## 🔄 Blog Post Lifecycle Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant PostService
    participant Database
    participant CommentService
    
    Client->>API: POST /posts (Create Draft)
    API->>PostService: create_post()
    PostService->>Database: Validate author
    Database-->>PostService: Author exists
    PostService->>Database: Save post (published=false)
    Database-->>PostService: Post created
    PostService-->>API: BlogPost object
    API-->>Client: 201 Created
    
    Client->>API: PUT /posts/{id} (Update)
    API->>PostService: update_post()
    PostService->>Database: Update post data
    Database-->>API: Updated post
    
    Client->>API: POST /posts/{id}/publish
    API->>PostService: publish_post()
    PostService->>Database: Set published=true
    Database-->>API: Published post
    
    Client->>API: GET /posts/{id}
    API->>PostService: get_post(increment_views=true)
    PostService->>Database: Increment view count
    PostService->>Database: Fetch post
    Database-->>Client: Post with updated views
    
    Client->>API: POST /comments (Add comment)
    API->>CommentService: create_comment()
    CommentService->>Database: Validate post & author
    CommentService->>Database: Save comment
    Database-->>Client: Comment created
```

## 🗄️ Data Model Relationships

```mermaid
erDiagram
    USER ||--o{ BLOG_POST : creates
    USER ||--o{ COMMENT : writes
    BLOG_POST ||--o{ COMMENT : has
    BLOG_POST }o--o{ TAG : tagged_with
    
    USER {
        int id PK
        string username UK
        string email
        string full_name
        datetime created_at
        boolean is_active
    }
    
    BLOG_POST {
        int id PK
        string title
        string content
        int author_id FK
        datetime created_at
        datetime updated_at
        boolean published
        int view_count
    }
    
    COMMENT {
        int id PK
        int post_id FK
        int author_id FK
        string content
        datetime created_at
        datetime updated_at
    }
    
    TAG {
        int id PK
        string name UK
        string slug
    }
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
# Run the development server
python -m uvicorn blog_api.main:app --reload

# Or run directly
python -m blog_api.main
```

The API will be available at:
- API Base: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 📚 API Endpoints

### Users
- `POST /users` - Create a new user
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get a specific user
- `GET /users/{user_id}/posts` - Get all posts by a user

### Blog Posts
- `POST /posts` - Create a new blog post
- `GET /posts` - Get all posts (with optional `published_only` filter)
- `GET /posts/{post_id}` - Get a specific post
- `PUT /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post
- `POST /posts/{post_id}/publish` - Publish a post
- `POST /posts/{post_id}/unpublish` - Unpublish a post

### Comments
- `POST /comments` - Create a new comment
- `GET /comments/{comment_id}` - Get a specific comment
- `GET /posts/{post_id}/comments` - Get all comments for a post
- `DELETE /comments/{comment_id}` - Delete a comment

### Tags
- `POST /tags` - Create a new tag
- `GET /tags` - Get all tags
- `GET /tags/{tag_id}` - Get a specific tag
- `GET /tags/{tag_id}/posts` - Get all posts with a tag

### Search
- `GET /search?q=query` - Search posts by title or content

### Statistics
- `GET /statistics` - Get overall blog statistics
- `GET /statistics/most-viewed` - Get most viewed posts
- `GET /statistics/most-commented` - Get most commented posts

## 🧪 Example Usage

### Create a User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }'
```

### Create a Blog Post
```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first post...",
    "author_id": 1,
    "published": true,
    "tags": [1, 2]
  }'
```

### Add a Comment
```bash
curl -X POST http://localhost:8000/comments \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": 1,
    "author_id": 2,
    "content": "Great post! Very informative."
  }'
```

### Search Posts
```bash
curl http://localhost:8000/search?q=fastapi
```

## 🔧 Key Features

- **RESTful API Design**: Clean, intuitive endpoints following REST principles
- **Data Validation**: Pydantic models ensure data integrity
- **Business Logic Separation**: Clear separation between API, service, and data layers
- **Thread-Safe Operations**: In-memory database with proper locking
- **Comprehensive Error Handling**: Detailed error messages and proper HTTP status codes
- **Interactive Documentation**: Auto-generated OpenAPI/Swagger docs
- **Search Functionality**: Full-text search across blog posts
- **Statistics & Analytics**: Built-in analytics for tracking engagement
- **Tag System**: Flexible tagging system for content organization

## 📁 Project Structure

```
blog_api/
├── __init__.py          # Package initialization
├── main.py              # FastAPI application and routes
├── models.py            # Pydantic data models
├── database.py          # In-memory database operations
└── services.py          # Business logic layer
```

## 🎯 Use Cases

This example is perfect for:
- **Code Review Practice**: Complex enough to demonstrate various code review scenarios
- **Learning FastAPI**: Demonstrates best practices and patterns
- **Microservice Template**: Can be adapted as a template for real services
- **API Design Examples**: Shows RESTful design patterns
- **Testing Scenarios**: Good foundation for writing tests

## 🔍 Code Review Focus Areas

When reviewing this code, consider:

1. **Architecture**: Is the separation of concerns clear?
2. **Data Flow**: How does data flow through the layers?
3. **Error Handling**: Are errors handled appropriately?
4. **Validation**: Is input validation comprehensive?
5. **Thread Safety**: Are concurrent operations handled safely?
6. **API Design**: Do endpoints follow REST principles?
7. **Documentation**: Is the code well-documented?
8. **Scalability**: Could this scale to a real database?

## 📝 Notes

- This uses an in-memory database for simplicity
- No authentication/authorization (would be added in production)
- Thread-safe but single-process (use Redis/PostgreSQL for multi-process)
- Sample data is pre-populated on startup

## 📄 License

This is a demonstration project for educational purposes.
