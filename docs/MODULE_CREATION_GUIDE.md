# KSeekers Backend - Complete Module Creation Guide

## Table of Contents
1. [Overview](#overview)
2. [Module Structure](#module-structure)
3. [Step-by-Step Module Creation](#step-by-step-module-creation)
4. [Database Integration](#database-integration)
5. [API Integration](#api-integration)
6. [Testing Your Module](#testing-your-module)
7. [Common Patterns](#common-patterns)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Overview

This guide provides a complete walkthrough for creating new modules in the KSeekers backend system. Each module follows a consistent 6-file structure and integrates seamlessly with the existing architecture.

### What You'll Learn
- How to create a complete module from scratch
- How to integrate with the database using migrations
- How to set up API endpoints with proper authentication
- How to follow the established patterns and conventions
- How to test and debug your new module

### Prerequisites
- Basic understanding of Python and FastAPI
- Familiarity with SQL and database concepts
- Understanding of the existing KSeekers architecture (see DEVELOPER_GUIDE.md)

---

## Module Structure

Every module in the KSeekers system follows this exact structure:

```
module_name/
├── __init__.py          # Package initialization file
├── module_models.py     # Data models (from_dict, to_dict methods)
├── module_schemas.py    # Pydantic schemas (request/response validation)
├── dao.py              # Data Access Object (database operations)
├── controller.py       # Business logic layer
├── routes.py          # API endpoints
└── query_helper.py    # Raw SQL query strings
```

**Note**: The `__init__.py` file is required to make the directory a Python package and should be created first.

### File Responsibilities

| File | Purpose | Contains |
|------|---------|----------|
| `__init__.py` | Package initialization | Package metadata and imports |
| `*_models.py` | Data structure definition | Classes with `from_dict()` and `to_dict()` methods |
| `*_schemas.py` | API validation | Pydantic models for request/response validation |
| `dao.py` | Database operations | Methods that interact with the database using raw SQL |
| `controller.py` | Business logic | Validation, processing, and orchestration |
| `routes.py` | API endpoints | FastAPI route definitions with authentication |
| `query_helper.py` | SQL queries | Static methods that return raw SQL strings |
---

## Step-by-Step Module Creation

Let's create a complete `products` module as an example. This will demonstrate every aspect of module creation.

### Step 1: Create Module Directory

```bash
# Create the module directory
mkdir -p products

# Navigate to the module directory
cd products

# Create the __init__.py file (required for Python package)
touch __init__.py

# Return to the backend root directory
cd ..
```

**Important**: Always create the `__init__.py` file first, as it's required for Python to recognize the directory as a package.

### Step 2: Create Database Migration

First, we need to create the database table for our products.

```bash
python run_migrations.py create --name "add_products_table"
```

This creates a new migration file. Edit the generated file:

**File: `migrations/02_add_products_table.sql`**
```sql
-- Migration: add_products_table
-- Version: 02
-- Created: 2024-12-01T12:00:00

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INT NULL,
    sku VARCHAR(100) UNIQUE NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category_id),
    INDEX idx_sku (sku),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data
INSERT INTO products (name, description, price, category_id, sku) VALUES
('Sample Product 1', 'This is a sample product description', 99.99, 1, 'SKU001'),
('Sample Product 2', 'Another sample product', 149.99, 2, 'SKU002'),
('Sample Product 3', 'Third sample product', 79.99, 1, 'SKU003')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

### Step 3: Run Migration

```bash
python run_migrations.py up
```

### Step 4: Create Models File

**File: `products/product_models.py`**
```python
from typing import Optional, Dict, Any
from datetime import datetime

class Product:
    """Product model for e-commerce system"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", description: str = "",
                 price: float = 0.0, category_id: Optional[int] = None, 
                 sku: Optional[str] = None, is_active: bool = True, 
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.sku = sku
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create Product instance from dictionary (database row)"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            description=data.get('description', ''),
            price=float(data.get('price', 0.0)),
            category_id=data.get('category_id'),
            sku=data.get('sku'),
            is_active=bool(data.get('is_active', True)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Product instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'sku': self.sku,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
```

### Step 5: Create Schemas File

**File: `products/product_schemas.py`**
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductCreate(BaseModel):
    """Schema for creating a new product"""
    name: str = Field(..., min_length=2, max_length=255, description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    category_id: Optional[int] = Field(None, description="Category ID")
    sku: Optional[str] = Field(None, max_length=100, description="Product SKU")

class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    sku: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    """Schema for product response"""
    id: int
    name: str
    description: str
    price: float
    category_id: Optional[int] = None
    sku: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ProductListResponse(BaseModel):
    """Schema for product list response"""
    products: List[ProductResponse]

class ProductByIdRequest(BaseModel):
    """Schema for product by ID request"""
    id: int = Field(..., gt=0, description="Product ID")

class ProductByCategoryRequest(BaseModel):
    """Schema for products by category request"""
    category_id: int = Field(..., gt=0, description="Category ID")

class ProductSearchRequest(BaseModel):
    """Schema for product search request"""
    query: str = Field(..., min_length=1, description="Search query")
    category_id: Optional[int] = Field(None, gt=0, description="Filter by category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
```

### Step 6: Create Query Helper File

**File: `products/query_helper.py`**
```python
class ProductQueryHelper:
    """Query helper for product-related database operations"""
    
    @staticmethod
    def create_product_query():
        """Returns SQL query for creating a new product"""
        return """
            INSERT INTO products (name, description, price, category_id, sku, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def get_product_by_id_query():
        """Returns SQL query for getting product by ID"""
        return "SELECT * FROM products WHERE id = %s LIMIT 1"
    
    @staticmethod
    def get_all_products_query():
        """Returns SQL query for getting all products"""
        return """
            SELECT * FROM products 
            WHERE is_active = 1 
            ORDER BY name
        """
    
    @staticmethod
    def get_products_by_category_query():
        """Returns SQL query for getting products by category"""
        return """
            SELECT * FROM products 
            WHERE category_id = %s AND is_active = 1
            ORDER BY name
        """
    
    @staticmethod
    def search_products_query():
        """Returns SQL query for searching products"""
        return """
            SELECT * FROM products 
            WHERE is_active = 1 
            AND (name LIKE %s OR description LIKE %s)
            AND (%s IS NULL OR category_id = %s)
            AND (%s IS NULL OR price >= %s)
            AND (%s IS NULL OR price <= %s)
            ORDER BY name
        """
    
    @staticmethod
    def update_product_query(set_clauses):
        """Returns SQL query for updating product"""
        return f"""
            UPDATE products 
            SET {', '.join(set_clauses)}, updated_at = %s
            WHERE id = %s
        """
    
    @staticmethod
    def delete_product_query():
        """Returns SQL query for soft deleting product"""
        return "UPDATE products SET is_active = 0, updated_at = %s WHERE id = %s"
    
    @staticmethod
    def get_product_by_sku_query():
        """Returns SQL query for getting product by SKU"""
        return "SELECT * FROM products WHERE sku = %s LIMIT 1"
    
    @staticmethod
    def check_sku_exists_query():
        """Returns SQL query for checking if SKU exists"""
        return "SELECT COUNT(*) as count FROM products WHERE sku = %s AND id != %s"
```

### Step 7: Create DAO File

**File: `products/dao.py`**
```python
import logging
from datetime import datetime
from manager.db_manager import DBManager
from products.product_models import Product
from products.query_helper import ProductQueryHelper

class ProductDAO:
    """Data Access Object for Product operations"""
    
    def __init__(self):
        self.db_manager = DBManager.get_instance()
    
    def create_product(self, name, description, price, category_id=None, sku=None):
        """Create a new product"""
        try:
            query = ProductQueryHelper.create_product_query()
            now = datetime.now()
            product_id = self.db_manager.execute_insert(query, (
                name, description, price, category_id, sku, True, now, now
            ))
            
            return Product(id=product_id, name=name, description=description, 
                          price=price, category_id=category_id, sku=sku)
        except Exception as e:
            logging.error(f"Error creating product: {e}")
            raise
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        try:
            query = ProductQueryHelper.get_product_by_id_query()
            result = self.db_manager.execute_query(query, (product_id,))
            
            if result:
                return Product.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting product by ID {product_id}: {e}")
            raise
    
    def get_all_products(self):
        """Get all active products"""
        try:
            query = ProductQueryHelper.get_all_products_query()
            results = self.db_manager.execute_query(query)
            
            return [Product.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting all products: {e}")
            raise
    
    def get_products_by_category(self, category_id):
        """Get products by category"""
        try:
            query = ProductQueryHelper.get_products_by_category_query()
            results = self.db_manager.execute_query(query, (category_id,))
            
            return [Product.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error getting products by category {category_id}: {e}")
            raise
    
    def search_products(self, query_text, category_id=None, min_price=None, max_price=None):
        """Search products with filters"""
        try:
            query = ProductQueryHelper.search_products_query()
            search_pattern = f"%{query_text}%"
            
            results = self.db_manager.execute_query(query, (
                search_pattern, search_pattern,  # name and description LIKE
                category_id, category_id,        # category filter
                min_price, min_price,           # min price filter
                max_price, max_price            # max price filter
            ))
            
            return [Product.from_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error searching products: {e}")
            raise
    
    def update_product(self, product_id, **kwargs):
        """Update product fields"""
        try:
            if not kwargs:
                return False
            
            set_clauses = []
            params = []
            
            for field, value in kwargs.items():
                if field in ['name', 'description', 'price', 'category_id', 'sku', 'is_active']:
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            params.append(datetime.now())  # updated_at
            params.append(product_id)      # WHERE id = ?
            
            query = ProductQueryHelper.update_product_query(set_clauses)
            rows_affected = self.db_manager.execute_update(query, params)
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating product {product_id}: {e}")
            raise
    
    def delete_product(self, product_id):
        """Soft delete product (set is_active = 0)"""
        try:
            query = ProductQueryHelper.delete_product_query()
            now = datetime.now()
            rows_affected = self.db_manager.execute_update(query, (now, product_id))
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error deleting product {product_id}: {e}")
            raise
    
    def get_product_by_sku(self, sku):
        """Get product by SKU"""
        try:
            query = ProductQueryHelper.get_product_by_sku_query()
            result = self.db_manager.execute_query(query, (sku,))
            
            if result:
                return Product.from_dict(result[0])
            return None
        except Exception as e:
            logging.error(f"Error getting product by SKU {sku}: {e}")
            raise
    
    def check_sku_exists(self, sku, exclude_id=None):
        """Check if SKU already exists"""
        try:
            query = ProductQueryHelper.check_sku_exists_query()
            exclude_id = exclude_id or 0
            result = self.db_manager.execute_query(query, (sku, exclude_id))
            
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            logging.error(f"Error checking SKU {sku}: {e}")
            raise
```

### Step 8: Create Controller File

**File: `products/controller.py`**
```python
from fastapi import HTTPException
from products.dao import ProductDAO
from products.product_models import Product

class ProductController:
    """Controller for product business logic"""
    
    def __init__(self):
        self.product_dao = ProductDAO()
    
    def create_product(self, name, description, price, category_id=None, sku=None):
        """Create a new product with validation"""
        # Business logic validation
        if not name or len(name.strip()) < 2:
            raise ValueError("Product name must be at least 2 characters")
        
        if price <= 0:
            raise ValueError("Product price must be positive")
        
        if sku and self.product_dao.check_sku_exists(sku):
            raise ValueError("SKU already exists")
        
        return self.product_dao.create_product(name, description, price, category_id, sku)
    
    def get_product(self, product_id):
        """Get product by ID"""
        if not product_id or product_id <= 0:
            raise ValueError("Invalid product ID")
        
        product = self.product_dao.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    
    def get_all_products(self):
        """Get all products"""
        return self.product_dao.get_all_products()
    
    def get_products_by_category(self, category_id):
        """Get products by category"""
        if not category_id or category_id <= 0:
            raise ValueError("Invalid category ID")
        
        return self.product_dao.get_products_by_category(category_id)
    
    def search_products(self, query_text, category_id=None, min_price=None, max_price=None):
        """Search products with filters"""
        if not query_text or len(query_text.strip()) < 1:
            raise ValueError("Search query must be at least 1 character")
        
        if min_price is not None and min_price < 0:
            raise ValueError("Minimum price cannot be negative")
        
        if max_price is not None and max_price < 0:
            raise ValueError("Maximum price cannot be negative")
        
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price")
        
        return self.product_dao.search_products(query_text, category_id, min_price, max_price)
    
    def update_product(self, product_id, **kwargs):
        """Update product with validation"""
        if not product_id or product_id <= 0:
            raise ValueError("Invalid product ID")
        
        # Check if product exists
        existing_product = self.product_dao.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate update data
        if 'price' in kwargs and kwargs['price'] <= 0:
            raise ValueError("Product price must be positive")
        
        if 'name' in kwargs and (not kwargs['name'] or len(kwargs['name'].strip()) < 2):
            raise ValueError("Product name must be at least 2 characters")
        
        if 'sku' in kwargs and kwargs['sku']:
            if self.product_dao.check_sku_exists(kwargs['sku'], product_id):
                raise ValueError("SKU already exists")
        
        return self.product_dao.update_product(product_id, **kwargs)
    
    def delete_product(self, product_id):
        """Delete product (soft delete)"""
        if not product_id or product_id <= 0:
            raise ValueError("Invalid product ID")
        
        # Check if product exists
        existing_product = self.product_dao.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return self.product_dao.delete_product(product_id)
```

### Step 9: Create Routes File

**File: `products/routes.py`**
```python
import time
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from utils.decorator import DecoratorUtils
from logical.logger import log_request, update_log
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage
from products.controller import ProductController
from products.product_schemas import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
    ProductByIdRequest, ProductByCategoryRequest, ProductSearchRequest
)
from logical.jwt_auth import JWTBearer, jwt_auth_required

class ProductRoutes:
    """Product API routes"""
    
    def __init__(self):
        self.app = APIRouter(prefix="/products", tags=["Products"])
        self.controller = ProductController()
        self.__add_routes()
    
    def __add_routes(self):
        # Create product
        self.app.add_api_route(
            path="/",
            endpoint=self.create_product,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Get all products
        self.app.add_api_route(
            path="/",
            endpoint=self.get_all_products,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Get product by ID
        self.app.add_api_route(
            path="/{product_id}",
            endpoint=self.get_product,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Update product
        self.app.add_api_route(
            path="/{product_id}",
            endpoint=self.update_product,
            methods=["PUT"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Delete product
        self.app.add_api_route(
            path="/{product_id}",
            endpoint=self.delete_product,
            methods=["DELETE"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Get products by category
        self.app.add_api_route(
            path="/category/{category_id}",
            endpoint=self.get_products_by_category,
            methods=["GET"],
            dependencies=[Depends(JWTBearer())]
        )
        
        # Search products
        self.app.add_api_route(
            path="/search",
            endpoint=self.search_products,
            methods=["POST"],
            dependencies=[Depends(JWTBearer())]
        )
    
    @log_request
    @jwt_auth_required
    async def create_product(self, request: Request, product_data: ProductCreate,
                           logger: str = Query(None, include_in_schema=False)):
        """Create a new product"""
        start_time = time.time()
        return_json = {}
        
        try:
            product = self.controller.create_product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                category_id=product_data.category_id,
                sku=product_data.sku
            )
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.created,
                rjson={"data": product.to_dict(), "error": [], "message": "Product created successfully"},
                row_count=1
            )
        except ValueError as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": ExceptionMessage.fail_to_create.value},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def get_all_products(self, request: Request,
                             logger: str = Query(None, include_in_schema=False)):
        """Get all products"""
        start_time = time.time()
        return_json = {}
        
        try:
            products = self.controller.get_all_products()
            product_dicts = [product.to_dict() for product in products]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": product_dicts, "error": [], "message": "Products retrieved successfully"},
                row_count=len(product_dicts)
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": "Error retrieving products"},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def get_product(self, request: Request, product_id: int,
                        logger: str = Query(None, include_in_schema=False)):
        """Get product by ID"""
        start_time = time.time()
        return_json = {}
        
        try:
            product = self.controller.get_product(product_id)
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": product.to_dict(), "error": [], "message": "Product retrieved successfully"},
                row_count=1
            )
        except HTTPException as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.not_found,
                rjson={"data": [], "error": [e.detail], "message": e.detail},
                row_count=0
            )
        except ValueError as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": "Error retrieving product"},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def update_product(self, request: Request, product_id: int, product_data: ProductUpdate,
                           logger: str = Query(None, include_in_schema=False)):
        """Update product"""
        start_time = time.time()
        return_json = {}
        
        try:
            # Convert Pydantic model to dict, excluding None values
            update_data = {k: v for k, v in product_data.dict().items() if v is not None}
            
            success = self.controller.update_product(product_id, **update_data)
            
            if success:
                # Get updated product
                updated_product = self.controller.get_product(product_id)
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": updated_product.to_dict(), "error": [], "message": "Product updated successfully"},
                    row_count=1
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.error,
                    rjson={"data": [], "error": ["No changes made"], "message": "No changes made"},
                    row_count=0
                )
        except HTTPException as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.not_found,
                rjson={"data": [], "error": [e.detail], "message": e.detail},
                row_count=0
            )
        except ValueError as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": "Error updating product"},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def delete_product(self, request: Request, product_id: int,
                           logger: str = Query(None, include_in_schema=False)):
        """Delete product"""
        start_time = time.time()
        return_json = {}
        
        try:
            success = self.controller.delete_product(product_id)
            
            if success:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.success,
                    rjson={"data": [], "error": [], "message": "Product deleted successfully"},
                    row_count=0
                )
            else:
                return_json = ReturnJson(
                    status_and_code=HTTPStatus.error,
                    rjson={"data": [], "error": ["Failed to delete product"], "message": "Failed to delete product"},
                    row_count=0
                )
        except HTTPException as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.not_found,
                rjson={"data": [], "error": [e.detail], "message": e.detail},
                row_count=0
            )
        except ValueError as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": "Error deleting product"},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def get_products_by_category(self, request: Request, category_id: int,
                                     logger: str = Query(None, include_in_schema=False)):
        """Get products by category"""
        start_time = time.time()
        return_json = {}
        
        try:
            products = self.controller.get_products_by_category(category_id)
            product_dicts = [product.to_dict() for product in products]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": product_dicts, "error": [], "message": f"Products for category {category_id} retrieved successfully"},
                row_count=len(product_dicts)
            )
        except ValueError as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": "Error retrieving products by category"},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
    
    @log_request
    @jwt_auth_required
    async def search_products(self, request: Request, search_data: ProductSearchRequest,
                            logger: str = Query(None, include_in_schema=False)):
        """Search products with filters"""
        start_time = time.time()
        return_json = {}
        
        try:
            products = self.controller.search_products(
                query_text=search_data.query,
                category_id=search_data.category_id,
                min_price=search_data.min_price,
                max_price=search_data.max_price
            )
            product_dicts = [product.to_dict() for product in products]
            
            return_json = ReturnJson(
                status_and_code=HTTPStatus.success,
                rjson={"data": product_dicts, "error": [], "message": "Product search completed successfully"},
                row_count=len(product_dicts)
            )
        except ValueError as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.bad_request,
                rjson={"data": [], "error": [str(e)], "message": str(e)},
                row_count=0
            )
        except Exception as e:
            return_json = ReturnJson(
                status_and_code=HTTPStatus.error,
                rjson={"data": [], "error": [str(e)], "message": "Error searching products"},
                row_count=0
            )
        finally:
            end_time = time.time()
            return_json.set_fetch_time((end_time - start_time))
            update_log(logger, return_json)
        
        return return_json.get_return_json()
```

### Step 10: Create Module Init File

**File: `products/__init__.py`**
```python
# This file makes the products directory a Python package
# It can be empty or contain package-level imports

__version__ = "1.0.0"
__author__ = "Your Name"
```

### Step 11: Register Module in Application

**Update `application.py`**
```python
# Add this import at the top
from products.routes import ProductRoutes

# Add this in the main function after other route registrations
app.include_router(ProductRoutes().app)
```
---

## Database Integration

### Migration Management

The KSeekers system uses a comprehensive migration system for database changes.

#### Creating Migrations

```bash
# Create a new migration
python run_migrations.py create --name "add_products_table"

# This creates: migrations/02_add_products_table.sql
```

#### Migration File Structure

```sql
-- Migration: add_products_table
-- Version: 02
-- Created: 2024-12-01T12:00:00

-- Your SQL statements here
CREATE TABLE products (...);
INSERT INTO products (...) VALUES (...);
```

#### Running Migrations

```bash
# Run all pending migrations
python run_migrations.py up

# Run migrations up to specific version
python run_migrations.py up --target 02

# Check migration status
python run_migrations.py status

# Rollback migrations
python run_migrations.py down
```

#### Rollback Migrations

Create rollback files for each migration:

**File: `migrations/R02_add_products_table.sql`**
```sql
-- Rollback migration for add_products_table
-- Version: R02
-- Created: 2024-12-01T12:00:00

DROP TABLE IF EXISTS products;
```

**Running Rollback Migrations:**
```bash
# Rollback to previous version
python run_migrations.py down

# Rollback to specific version
python run_migrations.py down --target 01

# Check rollback status
python run_migrations.py status
```
### Database Schema Best Practices

#### 1. Table Design
```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INT NULL,
    sku VARCHAR(100) UNIQUE NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_name (name),
    INDEX idx_category (category_id),
    INDEX idx_sku (sku),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 2. Foreign Key Constraints
```sql
-- Add foreign key constraint
ALTER TABLE products 
ADD CONSTRAINT fk_products_category 
FOREIGN KEY (category_id) REFERENCES categories(id) 
ON DELETE SET NULL ON UPDATE CASCADE;
```

#### 3. Data Validation
```sql
-- Add check constraints
ALTER TABLE products 
ADD CONSTRAINT chk_price_positive 
CHECK (price > 0);

ALTER TABLE products 
ADD CONSTRAINT chk_name_length 
CHECK (CHAR_LENGTH(name) >= 2);
```
---

## API Integration

### Authentication Integration

All API endpoints use JWT authentication:

```python
from logical.jwt_auth import JWTBearer, jwt_auth_required

# In route definitions
@jwt_auth_required
async def protected_endpoint(self, request: Request, ...):
    # Your endpoint logic
```

### Response Format

All endpoints return standardized responses using `ReturnJson`:

```python
return_json = ReturnJson(
    status_and_code=HTTPStatus.success,
    rjson={"data": result_data, "error": [], "message": "Success message"},
    row_count=len(result_data)
)
```

### Error Handling

```python
try:
    # Your logic
    result = self.controller.some_method()
except ValueError as e:
    return_json = ReturnJson(
        status_and_code=HTTPStatus.bad_request,
        rjson={"data": [], "error": [str(e)], "message": str(e)},
        row_count=0
    )
except HTTPException as e:
    return_json = ReturnJson(
        status_and_code=HTTPStatus.not_found,
        rjson={"data": [], "error": [e.detail], "message": e.detail},
        row_count=0
    )
except Exception as e:
    return_json = ReturnJson(
        status_and_code=HTTPStatus.error,
        rjson={"data": [], "error": [str(e)], "message": "Unexpected error"},
        row_count=0
    )
```
---

## Testing Your Module

### 1. Test Database Connection

```bash
python -c "from manager.db_manager import DBManager; print('DB OK' if DBManager.get_instance().execute_query('SELECT 1') else 'DB Error')"
```

### 2. Test Migration

```bash
# Check migration status
python run_migrations.py status

# Run migrations
python run_migrations.py up

# Verify table exists
python -c "from manager.db_manager import DBManager; print(DBManager.get_instance().execute_query('DESCRIBE products'))"
```

### 3. Test API Endpoints

Start the application:

```bash
python application.py
```

Test endpoints using curl or Postman:

```bash
# Get authentication token first
curl -X POST "http://localhost:8000/auth/otp/request" \
  -H "Content-Type: application/json" \
  -d '{"username_or_email": "admin"}'

# Verify OTP and get token
curl -X POST "http://localhost:8000/auth/otp/verify" \
  -H "Content-Type: application/json" \
  -d '{"username_or_email": "admin", "otp_code": "123456"}'

# Test product endpoints
curl -X GET "http://localhost:8000/products/" \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "description": "Test Description", "price": 99.99}'
```

### 4. Test Business Logic

```python
# Test controller directly
from products.controller import ProductController

controller = ProductController()

# Test product creation
product = controller.create_product("Test Product", "Test Description", 99.99)
print(f"Created product: {product.to_dict()}")

# Test product retrieval
retrieved = controller.get_product(product.id)
print(f"Retrieved product: {retrieved.to_dict()}")
```

### 5. Test Complete Module Integration

```python
# Test the complete module flow
from products.routes import ProductRoutes
from products.product_schemas import ProductCreate

# Create routes instance
routes = ProductRoutes()

# Test schema validation
product_data = ProductCreate(
    name="Integration Test Product",
    description="Testing complete module integration",
    price=199.99,
    category_id=1,
    sku="INTEGRATION_TEST_001"
)

print("Schema validation passed:", product_data.dict())
```
---

## Common Patterns

### 1. CRUD Operations Pattern

Every module should implement these standard operations:

- **Create**: `create_entity()`
- **Read**: `get_entity_by_id()`, `get_all_entities()`, `search_entities()`
- **Update**: `update_entity()`
- **Delete**: `delete_entity()` (soft delete)

### 2. Validation Pattern

```python
def create_entity(self, **kwargs):
    # Validate required fields
    if not kwargs.get('name'):
        raise ValueError("Name is required")
    
    # Validate data types and ranges
    if kwargs.get('price', 0) <= 0:
        raise ValueError("Price must be positive")
    
    # Validate business rules
    if self.dao.check_exists(kwargs.get('unique_field')):
        raise ValueError("Entity already exists")
    
    return self.dao.create_entity(**kwargs)
```

### 3. Error Handling Pattern

```python
try:
    result = self.controller.some_operation()
    return_json = ReturnJson(
        status_and_code=HTTPStatus.success,
        rjson={"data": result, "error": [], "message": "Success"},
        row_count=1
    )
except ValueError as e:
    return_json = ReturnJson(
        status_and_code=HTTPStatus.bad_request,
        rjson={"data": [], "error": [str(e)], "message": str(e)},
        row_count=0
    )
except HTTPException as e:
    return_json = ReturnJson(
        status_and_code=HTTPStatus.not_found,
        rjson={"data": [], "error": [e.detail], "message": e.detail},
        row_count=0
    )
except Exception as e:
    return_json = ReturnJson(
        status_and_code=HTTPStatus.error,
        rjson={"data": [], "error": [str(e)], "message": "Unexpected error"},
        row_count=0
    )
```

### 4. Query Helper Pattern

```python
class EntityQueryHelper:
    @staticmethod
    def create_entity_query():
        return "INSERT INTO entities (field1, field2) VALUES (%s, %s)"
    
    @staticmethod
    def get_entity_by_id_query():
        return "SELECT * FROM entities WHERE id = %s LIMIT 1"
    
    @staticmethod
    def update_entity_query(set_clauses):
        return f"UPDATE entities SET {', '.join(set_clauses)} WHERE id = %s"
```
---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'products'`

**Solution**: Ensure the module directory is in the Python path and has an `__init__.py` file:

```bash
# Create the __init__.py file
touch products/__init__.py

# Or if the directory doesn't exist yet
mkdir -p products
touch products/__init__.py
```

#### 2. Database Connection Issues

**Problem**: `(1045, "Access denied for user 'user'@'localhost'")`

**Solution**: Check your `.env` file database credentials:

```bash
# Check .env file
cat .env | grep db_

# Test connection
python -c "from manager.db_manager import DBManager; print(DBManager.get_instance().execute_query('SELECT 1'))"
```

#### 3. Migration Issues

**Problem**: `Migration failed at version 02`

**Solution**: Check SQL syntax and run manually:

```bash
# Check migration file syntax
cat migrations/02_add_products_table.sql

# Test SQL manually
mysql -u root -p -e "USE kseekers; SOURCE migrations/02_add_products_table.sql;"
```

#### 4. Authentication Issues

**Problem**: `401 Unauthorized`

**Solution**: Ensure JWT token is valid and properly formatted:

```bash
# Check token format
echo "Authorization: Bearer YOUR_TOKEN"

# Test authentication
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 5. Validation Errors

**Problem**: `422 Unprocessable Entity`

**Solution**: Check Pydantic schema validation:

```python
# Test schema validation
from products.product_schemas import ProductCreate

try:
    product = ProductCreate(name="Test", description="Test", price=99.99)
    print("Schema validation passed")
except Exception as e:
    print(f"Schema validation failed: {e}")
```

#### 6. Module Import Issues

**Problem**: `ImportError: cannot import name 'ProductController' from 'products.controller'`

**Solution**: Check that all files are properly created and imports are correct:

```bash
# Verify all files exist
ls -la products/

# Check for syntax errors
python -m py_compile products/controller.py
python -m py_compile products/dao.py
python -m py_compile products/routes.py
```

#### 7. Database Connection Issues

**Problem**: `ConnectionError: Failed to connect to database`

**Solution**: Verify database configuration and connection:

```python
# Test database connection
from manager.db_manager import DBManager

try:
    db = DBManager.get_instance()
    result = db.execute_query("SELECT 1")
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
```
### Debugging Tips

#### 1. Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 2. Test Individual Components

```python
# Test DAO directly
from products.dao import ProductDAO
dao = ProductDAO()
result = dao.get_all_products()
print(f"DAO result: {result}")

# Test Controller directly
from products.controller import ProductController
controller = ProductController()
result = controller.get_all_products()
print(f"Controller result: {result}")
```

#### 3. Check Database State

```bash
# Check table structure
mysql -u root -p -e "USE kseekers; DESCRIBE products;"

# Check data
mysql -u root -p -e "USE kseekers; SELECT * FROM products LIMIT 5;"
```
---

## Best Practices

### 1. Module Organization

- **Keep modules focused**: Each module should handle one business domain
- **Follow naming conventions**: Use descriptive, consistent names
- **Maintain separation of concerns**: Don't mix business logic with data access

### 2. Database Design

- **Use proper indexing**: Add indexes for frequently queried columns
- **Implement soft deletes**: Use `is_active` flags instead of hard deletes
- **Add audit fields**: Include `created_at` and `updated_at` timestamps
- **Use foreign keys**: Maintain referential integrity

### 3. API Design

- **Use RESTful conventions**: Follow standard HTTP methods and status codes
- **Implement proper validation**: Use Pydantic schemas for request/response validation
- **Handle errors gracefully**: Provide meaningful error messages
- **Use consistent response format**: Always use `ReturnJson` for responses

### 4. Security

- **Authenticate all endpoints**: Use JWT authentication for protected routes
- **Validate input data**: Always validate and sanitize user input
- **Use parameterized queries**: Prevent SQL injection attacks
- **Implement rate limiting**: Protect against abuse and DoS attacks

### 5. Performance

- **Use connection pooling**: Efficiently manage database connections
- **Implement caching**: Cache frequently accessed data
- **Optimize queries**: Use proper indexes and query patterns
- **Monitor performance**: Track response times and resource usage

### 6. Testing

- **Write unit tests**: Test individual components in isolation
- **Write integration tests**: Test component interactions
- **Test error scenarios**: Ensure proper error handling
- **Use test data**: Create realistic test datasets

### 7. Documentation

- **Document APIs**: Use clear, comprehensive API documentation
- **Add code comments**: Explain complex business logic
- **Maintain README files**: Keep project documentation up to date
- **Use type hints**: Improve code readability and IDE support

---

## Conclusion

This guide provides a comprehensive walkthrough for creating new modules in the KSeekers backend system. By following these patterns and practices, you can:

- Create consistent, maintainable modules
- Integrate seamlessly with the existing architecture
- Implement proper database migrations
- Build secure, performant APIs
- Follow established coding standards

Remember to always test your modules thoroughly and follow the established patterns for consistency across the codebase.

For additional help, refer to the `DEVELOPER_GUIDE.md` for detailed information about the overall system architecture and existing modules.

---

## Module Creation Checklist

Use this checklist to ensure you've completed all necessary steps when creating a new module:

### ✅ **Pre-Creation**
- [ ] Understand the business requirements
- [ ] Plan the database schema
- [ ] Identify required API endpoints
- [ ] Review existing modules for patterns

### ✅ **Module Structure**
- [ ] Create module directory
- [ ] Create `__init__.py` file
- [ ] Create `*_models.py` file
- [ ] Create `*_schemas.py` file
- [ ] Create `query_helper.py` file
- [ ] Create `dao.py` file
- [ ] Create `controller.py` file
- [ ] Create `routes.py` file

### ✅ **Database Integration**
- [ ] Create migration file
- [ ] Run migration
- [ ] Test database connection
- [ ] Verify table structure
- [ ] Test CRUD operations

### ✅ **API Integration**
- [ ] Register routes in `application.py`
- [ ] Test authentication
- [ ] Test all endpoints
- [ ] Verify response format
- [ ] Test error handling

### ✅ **Testing & Validation**
- [ ] Test individual components
- [ ] Test complete module flow
- [ ] Test error scenarios
- [ ] Verify business logic
- [ ] Test with real data

### ✅ **Documentation & Cleanup**
- [ ] Add code comments
- [ ] Update API documentation
- [ ] Test module integration
- [ ] Remove test data
- [ ] Verify production readiness

---

## Quick Reference

### **Module File Template**
```bash
# Create new module
mkdir -p module_name
cd module_name
touch __init__.py
touch module_models.py
touch module_schemas.py
touch query_helper.py
touch dao.py
touch controller.py
touch routes.py
cd ..
```

### **Common Commands**
```bash
# Create migration
python run_migrations.py create --name "add_module_table"

# Run migrations
python run_migrations.py up

# Check migration status
python run_migrations.py status

# Test database connection
python -c "from manager.db_manager import DBManager; print('DB OK' if DBManager.get_instance().execute_query('SELECT 1') else 'DB Error')"

# Start application
python application.py
```

### **Import Pattern**
```python
# In dao.py
from module_name.module_models import ModuleModel
from module_name.query_helper import ModuleQueryHelper

# In controller.py
from module_name.dao import ModuleDAO
from module_name.module_models import ModuleModel

# In routes.py
from module_name.controller import ModuleController
from module_name.module_schemas import ModuleCreate, ModuleUpdate
```