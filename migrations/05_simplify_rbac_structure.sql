-- Migration: Add Module Support to RBAC
-- Version: 05
-- Created: 2024-12-01T16:00:00
-- Description: Add module concept to RBAC system while keeping existing structure

-- Start transaction
START TRANSACTION;

-- Step 1: Add module field to rights table (if it doesn't exist)
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'rights' 
  AND COLUMN_NAME = 'module';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE rights ADD COLUMN module VARCHAR(100) NOT NULL DEFAULT ''default'' COMMENT ''Module this right belongs to''', 
    'SELECT ''Column module already exists'' as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 2: Add index for module field (if it doesn't exist)
SET @index_exists = 0;
SELECT COUNT(*) INTO @index_exists 
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'rights' 
  AND INDEX_NAME = 'idx_rights_module';

SET @sql = IF(@index_exists = 0, 
    'CREATE INDEX idx_rights_module ON rights(module)', 
    'SELECT ''Index idx_rights_module already exists'' as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 3: Add role field to users table if it doesn't exist
-- First check if column exists, then add if it doesn't
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'users' 
  AND COLUMN_NAME = 'role_id';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE users ADD COLUMN role_id INT NULL COMMENT ''User role ID''', 
    'SELECT ''Column role_id already exists'' as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 4: Add foreign key constraint for user role (if it doesn't exist)
SET @constraint_exists = 0;
SELECT COUNT(*) INTO @constraint_exists 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'users' 
  AND CONSTRAINT_NAME = 'fk_users_role_id';

SET @sql = IF(@constraint_exists = 0, 
    'ALTER TABLE users ADD CONSTRAINT fk_users_role_id FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL', 
    'SELECT ''Constraint fk_users_role_id already exists'' as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 5: Add index for user role (if it doesn't exist)
SET @index_exists = 0;
SELECT COUNT(*) INTO @index_exists 
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'users' 
  AND INDEX_NAME = 'idx_users_role_id';

SET @sql = IF(@index_exists = 0, 
    'CREATE INDEX idx_users_role_id ON users(role_id)', 
    'SELECT ''Index idx_users_role_id already exists'' as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 6: Update existing wildcard right to include module
UPDATE rights 
SET module = 'system'
WHERE name = '*';

-- Step 7: Add comments for documentation
ALTER TABLE rights COMMENT = 'System rights/permissions for RBAC with module support';
ALTER TABLE users COMMENT = 'Users table with single role assignment';

-- Commit transaction
COMMIT;