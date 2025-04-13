from functools import wraps
import time
from datetime import datetime
from typing import Any, Callable, Dict, Optional
import logging
import os
from fastapi import Request

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