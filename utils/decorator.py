from functools import wraps
import time
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Union, List
import logging
import os
from fastapi import Request, HTTPException, Query
from models.returnjson import ReturnJson
from models.enums import HTTPStatus, ExceptionMessage
from logical.logger import log_request, update_log

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DecoratorUtils:
    @staticmethod
    def highlighted_print(message: str) -> None:
        """Print a message with highlighted formatting."""
        print(f"\n{'-'*100}")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} :::: {message}")
        print(f"{'-'*100}\n")

    @staticmethod
    def profile(func: Callable) -> Callable:
        """
        Decorator to profile API endpoints.
        Measures execution time and logs request/response data.
        """
        # Get function information at decoration time
        module_name = func.__module__
        line_number = func.__code__.co_firstlineno
        
        import inspect
        is_coroutine = inspect.iscoroutinefunction(func)
        
        if is_coroutine:
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                start_time = time.time()
                start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Extract request data if available
                request_data: Optional[Dict] = None
                for arg in args:
                    if isinstance(arg, Request):
                        try:
                            request_data = await arg.json()
                        except Exception:
                            request_data = None
                        break
                
                try:
                    # Execute the function
                    result = await func(*args, **kwargs)
                    
                    end_time = time.time()
                    end_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Log profiling information
                    DecoratorUtils.highlighted_print(
                        f"Method:: {func.__name__}\n"
                        f"Module:: {module_name}:{line_number}\n"
                        f"Request Time:: {start_dt}\n"
                        f"Response Time:: {end_dt}\n"
                        f"Execution Time:: {end_time - start_time:.4f} seconds\n"
                        f"Request Data:: {request_data}\n"
                        f"Response Data:: {str(result)}"
                    )
                    
                    # Return the original result without modification
                    return result
                    
                except Exception as e:
                    logger.error(f"Error in profiling {func.__name__}: {str(e)}")
                    # Re-raise the exception to maintain normal error handling
                    raise
                    
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                start_time = time.time()
                start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Extract request data if available (unlikely in sync functions)
                request_data: Optional[Dict] = None
                
                try:
                    # Execute the function
                    result = func(*args, **kwargs)
                    
                    end_time = time.time()
                    end_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Log profiling information
                    DecoratorUtils.highlighted_print(
                        f"Method:: {func.__name__}\n"
                        f"Module:: {module_name}:{line_number}\n"
                        f"Request Time:: {start_dt}\n"
                        f"Response Time:: {end_dt}\n"
                        f"Execution Time:: {end_time - start_time:.4f} seconds\n"
                        f"Args:: {args}\n"
                        f"Response Data:: {str(result)}"
                    )
                    
                    # Return the original result without modification
                    return result
                    
                except Exception as e:
                    logger.error(f"Error in profiling {func.__name__}: {str(e)}")
                    # Re-raise the exception to maintain normal error handling
                    raise
                    
            return sync_wrapper

    @staticmethod
    def api_response(
            success_message: str = "Operation completed successfully",
            error_message: str = "An error occurred",
            success_status: HTTPStatus = HTTPStatus.success,
            error_status: HTTPStatus = HTTPStatus.error,
            include_data: bool = True
        ):
        """
        Decorator to standardize API response handling across all endpoints.
        
        Args:
            success_message: Message to return on successful operation
            error_message: Message to return on error
            success_status: HTTP status for successful operations
            error_status: HTTP status for errors
            include_data: Whether to include data in response (for delete operations)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
                start_time = time.time()
                return_json = {}
                
                # Extract logger from kwargs if present
                logger_param = kwargs.get('logger')
                
                try:
                    # Execute the controller method
                    result = await func(*args, **kwargs)
                    
                    # Handle different result types
                    if result is None:
                        # No data returned (e.g., delete operations)
                        return_json = ReturnJson(
                            status_and_code=success_status,
                            rjson={"data": [], "error": [], "message": success_message},
                            row_count=0
                        )
                    elif isinstance(result, (list, tuple)):
                        # List of objects returned
                        if include_data and result:
                            # Convert objects to dict if they have to_dict method
                            if hasattr(result[0], 'to_dict'):
                                data = [item.to_dict() for item in result]
                            else:
                                data = result
                        else:
                            data = result if include_data else []
                        
                        return_json = ReturnJson(
                            status_and_code=success_status,
                            rjson={"data": data, "error": [], "message": success_message},
                            row_count=len(result)
                        )
                    elif isinstance(result, dict):
                        # Dictionary returned (e.g., permissions, stats)
                        return_json = ReturnJson(
                            status_and_code=success_status,
                            rjson={"data": result, "error": [], "message": success_message},
                            row_count=len(result) if isinstance(result, (list, dict)) else 1
                        )
                    else:
                        # Single object returned
                        if hasattr(result, 'to_dict'):
                            data = result.to_dict()
                        else:
                            data = result
                        
                        return_json = ReturnJson(
                            status_and_code=success_status,
                            rjson={"data": data, "error": [], "message": success_message},
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
                        status_and_code=e.status_code,
                        rjson={"data": [], "error": [e.detail], "message": e.detail},
                        row_count=0
                    )
                except Exception as e:
                    return_json = ReturnJson(
                        status_and_code=error_status,
                        rjson={"data": [], "error": [str(e)], "message": error_message},
                        row_count=0
                    )
                finally:
                    end_time = time.time()
                    return_json.set_fetch_time((end_time - start_time))
                    if logger_param:
                        update_log(logger_param, return_json)
                
                return return_json.get_return_json()
            
            return wrapper
        return decorator

    @staticmethod
    def create_endpoint(
        success_message: str = "Operation completed successfully",
        error_message: str = "An error occurred",
        success_status: HTTPStatus = HTTPStatus.success,
        error_status: HTTPStatus = HTTPStatus.error,
        include_data: bool = True
    ):
        """
        Decorator factory for creating standardized API endpoints.
        Combines @log_request, @jwt_auth_required, and @api_response decorators.
        """
        def decorator(func: Callable) -> Callable:
            # Apply the decorators in the correct order
            decorated_func = log_request(func)
            decorated_func = DecoratorUtils.api_response(
                success_message=success_message,
                error_message=error_message,
                success_status=success_status,
                error_status=error_status,
                include_data=include_data
            )(decorated_func)
            
            return decorated_func
        return decorator 