import os
import sys
from dotenv import load_dotenv

# Check command line arguments for environment selection
try:
    env_selection = sys.argv[1] if len(sys.argv) > 1 else 'env'
except:
    env_selection = 'env'

# Select environment file
if env_selection == 'dev':
    print('dev is selected')
    env_file = '.dev'
elif env_selection == 'prod':
    print('prod is selected')
    env_file = '.prod'
else:
    print('local ENV Activated')
    env_file = '.env'

# Load the selected environment file
load_dotenv(env_file, override=True)

# SSL Configuration (Currently unused)
# ssl_key = ""
# ssl_cert = ""
# if os.getenv('secureEnv') == 'True':
#     print('SSL is Activated')
#     ssl_key = os.getenv('ssl_keyfile')
#     ssl_cert = os.getenv('ssl_certfile')
# else:
#     print('SSL NOT Activated')

# AWS S3 configuration
aws_region = os.getenv('aws_region')
s3_user_access_key = os.getenv('s3_user_access_key')
s3_user_access_secret = os.getenv('s3_user_access_secret')
s3_bucket_name = os.getenv('pdf_bucket_name')
# presigned_url_timeout = 600  # Currently unused

# Database configuration - MySQL (Primary)
db_host = os.getenv('db_host', 'localhost')
db_port = os.getenv('db_port', '3306')
db_user = os.getenv('db_user', 'root')
db_password = os.getenv('db_password', '')
ks_database = os.getenv('ks_database', 'kseekers')
db_conn_pool = int(os.getenv('DB_CONN_POOL', '5'))
db_conn_pool_max = int(os.getenv('DB_CONN_POOL_MAX', '10'))
# db_echo = os.getenv('DB_ECHO', 'False').lower() == 'true'  # Currently unused

# Migration configuration (Currently unused)
# migrations_dir = os.getenv('MIGRATIONS_DIR', 'migrations')

# JWT configuration
# IMPORTANT: Change the default secret in production environments
secret = os.getenv('secret', 'your-default-jwt-secret-key-change-in-production')
algorithm = os.getenv('algorithm', 'HS256')
expiry = int(os.getenv('jwt_expiry', 2 * 60 * 60)) # 2 hours Default

# Logging configuration
logging_path = os.getenv('logging_path', 'logs/app.log')
logging_file_size = int(os.getenv('logging_file_size', '10485760'))  # 10MB default
logging_backup_count = int(os.getenv('logging_backup_count', '5'))


