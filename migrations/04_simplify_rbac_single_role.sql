-- Migration: Simplify RBAC to Single Role Per User
-- Version: 04
-- Created: 2024-12-01T16:00:00
-- Description: Remove user_roles table and add role column to users table for single role assignment

-- Start transaction
START TRANSACTION;

-- Step 1: Add role column to users table
ALTER TABLE users 
ADD COLUMN role VARCHAR(100) NULL COMMENT 'User role (references roles.name)',
ADD INDEX idx_role (role);

-- Step 2: Set super_admin role for all existing users (since we're simplifying to single role)
UPDATE users 
SET role = 'super_admin' 
WHERE role IS NULL;

-- Step 3: Drop the user_roles table if it exists (no longer needed)
DROP TABLE IF EXISTS user_roles;

-- Step 4: Add foreign key constraint for role column (optional, for data integrity)
-- Note: This is commented out as it might cause issues if roles are deleted
-- ALTER TABLE users 
-- ADD CONSTRAINT fk_users_role FOREIGN KEY (role) REFERENCES roles(name) ON UPDATE CASCADE;

-- Step 5: Update comments
ALTER TABLE users COMMENT = 'Users table with single role assignment';
ALTER TABLE roles COMMENT = 'System roles for RBAC - single role per user';

-- Step 6: Create indexes for better performance
CREATE INDEX idx_users_role_active ON users(role, is_active);

-- Commit transaction
COMMIT;
