# KSeekers Backend

A FastAPI backend application for KSeekers with MySQL support and custom connection pooling.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- MySQL 5.7+ or MySQL 8.0+
- mysql-connector-python driver (included in requirements.txt)

### Installation

1. Clone the repository
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file with your MySQL configuration (see `.env.example`)
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

### MySQL Database with Connection Pooling

The application uses MySQL as the primary database with a custom connection pool implementation for better performance. The connection pool:

- Pre-creates a fixed number of database connections
- Manages connection reuse across multiple operations
- Provides direct SQL query capabilities with parameterized queries
- Supports comprehensive migration system for schema management

Example usage:

```python
# Using the connection pool for direct SQL queries
db_manager = DBManager.get_instance()
results = db_manager.execute_query("SELECT * FROM my_table WHERE id = %s", (my_id,))

# Using context managers for transactions
with get_db_transaction() as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    # Transaction is automatically committed
```

### Database Migration System

The application includes a comprehensive migration system for managing database schema changes:

#### Running Migrations

```bash
# Run all pending migrations
python run_migrations.py up

# Run migrations up to a specific version
python run_migrations.py up --target V20241201000003

# Rollback migrations
python run_migrations.py down

# Rollback to a specific version
python run_migrations.py down --target V20241201000002

# Check migration status
python run_migrations.py status

# Create a new migration
python run_migrations.py create --name "add_new_table"
```

#### Migration Files

Migration files are stored in the `migrations/` directory with simple numbering:
- `01_initial_schema.sql` - Initial database schema and sample data
- `02_{name}.sql` - Future migrations
- `03_{name}.sql` - And so on...

### Database Setup

The `setup_database.py` script:
1. Creates the MySQL database if it doesn't exist
2. Runs all pending migrations
3. Verifies the final migration status

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

## Documentation

All API documentation and guides are located in the `docs/` folder:

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference with examples
- **[Postman Collection](docs/KSeekers_API_Documentation.postman_collection.json)** - Import into Postman for testing
- **[Postman Environment](docs/KSeekers_Environment.postman_environment.json)** - Environment variables for Postman
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Development setup and guidelines
- **[Module Creation Guide](docs/MODULE_CREATION_GUIDE.md)** - How to create new modules
- **[Table Structure Guide](docs/TABLE_STRUCTURE_MODIFICATION_GUIDE.md)** - Database schema management

## API Modules

### Authentication (`/auth`)
- User registration and OTP-based login
- JWT token management

### Lookup (`/lookup`) 
- Lookup types and values management
- Full CRUD operations for configuration data

### Display Config (`/display-config`)
- Grid configuration management
- Display settings for data tables

## Authentication

JWT-based authentication is implemented for secure API endpoints. See the [API Documentation](docs/API_DOCUMENTATION.md) for detailed authentication flow.

## Future MySQL Migration

To migrate to MySQL in the future:
1. Update the `.env` file with MySQL connection details
2. Modify the `DBManager.get_engine()` method in `manager/db_manager.py` to use the MySQL connection string
3. Create the equivalent tables in MySQL using the schema defined in `setup_database.py` 