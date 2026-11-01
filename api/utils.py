from rest_framework.response import Response
from rest_framework import status
from functools import wraps

# Shared secret key used by your web frontend, python backend, and ESP32
LOCAL_API_KEY = "qr-medsecure-super-secret-key-123"

def require_api_key(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        client_api_key = request.headers.get("X-API-Key")
        
        if not client_api_key or client_api_key != LOCAL_API_KEY:
            return Response(
                {"error": "Unauthorized. Invalid or missing API Key."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return wrapper