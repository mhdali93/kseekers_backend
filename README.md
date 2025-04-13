# Scholar Dental Backend

A FastAPI backend application for Scholar Dental with SQLite support and custom connection pooling.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- SQLite3 (default database, included in Python)
- MySQL (optional, for future use)

### Installation

1. Clone the repository
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration (see `.env.example`)
4. Set up the database:

```
python setup_database.py
```

5. Run the application:

```
python application.py
```

### Environment Configuration

You can specify which environment to use when starting the application:

- Development environment: `python application.py dev`
- Production environment: `python application.py prod`
- Local environment: `python application.py` (default)

## Database System

### SQLite Database with Connection Pooling

The application uses SQLite as the default database with a custom connection pool implementation for better performance. The connection pool:

- Pre-creates a fixed number of database connections
- Manages connection reuse across multiple operations
- Provides both SQLModel ORM support and direct SQL query capabilities
- Supports easy migration to MySQL in the future

Example usage:

```python
# Using the connection pool for direct SQL queries
db_manager = DBManager.get_instance()
results = db_manager.execute_query("SELECT * FROM my_table WHERE id = ?", (my_id,))

# Using SQLModel with session management
with DBSessionManager() as session:
    results = session.exec(select(MyModel).where(MyModel.id == my_id)).all()
```

### Database Setup

The `setup_database.py` script creates the SQLite database and necessary tables. It also populates the database with sample data for:

- Result display configurations
- Lookup types and values

Run it with:
```
python setup_database.py
```

## Using AWS S3 Functionality

The application includes an S3Handler class for file operations with AWS S3. Here's how to use it:

```python
from logical.s3_handler import S3Handler

# Upload a file to S3
S3Handler.upload_file('/path/to/local/file.pdf', 'destination/path/file.pdf')

# Upload a file-like object to S3
with open('example.pdf', 'rb') as file_obj:
    S3Handler.upload_fileobj(file_obj, 'destination/path/example.pdf')

# Generate a presigned URL for downloading a file (valid for 1 hour by default)
download_url = S3Handler.generate_presigned_url('path/to/file.pdf')

# Delete a file from S3
S3Handler.delete_object('path/to/file.pdf')
```

Required AWS configuration in your .env file:

```
aws_region=us-east-1
s3_user_access_key=YOUR_ACCESS_KEY
s3_user_access_secret=YOUR_SECRET_KEY
pdf_bucket_name=your-bucket-name
```

## API Endpoints

- Health Check: `/healthCheck` (GET)
- Look Up Headers: `/getHeaders?type={type}` (GET) - Requires JWT authentication

## Authentication

JWT-based authentication is implemented for secure API endpoints.

## Future MySQL Migration

To migrate to MySQL in the future:
1. Update the `.env` file with MySQL connection details
2. Modify the `DBManager.get_engine()` method in `manager/db_manager.py` to use the MySQL connection string
3. Create the equivalent tables in MySQL using the schema defined in `setup_database.py` 