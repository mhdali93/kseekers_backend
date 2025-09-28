-- Migration: Add Module Support to RBAC
-- Version: 05
-- Created: 2024-12-01T16:00:00
-- Description: Add module concept to RBAC system while keeping existing structure

-- Step 1: Add module field to rights table
ALTER TABLE rights 
ADD COLUMN module VARCHAR(100) NOT NULL DEFAULT 'default' COMMENT 'Module this right belongs to';

-- Step 2: Add index for module field
CREATE INDEX idx_rights_module ON rights(module);

-- Step 3: Add role field to users table if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS role_id INT NULL COMMENT 'User role ID';

-- Step 4: Add foreign key constraint for user role
ALTER TABLE users 
ADD CONSTRAINT fk_users_role_id 
FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL;

-- Step 5: Add index for user role
CREATE INDEX idx_users_role_id ON users(role_id);

-- Step 6: Update existing wildcard right to include module
UPDATE rights 
SET module = 'system'
WHERE name = '*';

-- Step 7: Add comments for documentation
ALTER TABLE rights COMMENT = 'System rights/permissions for RBAC with module support';
ALTER TABLE users COMMENT = 'Users table with single role assignment';