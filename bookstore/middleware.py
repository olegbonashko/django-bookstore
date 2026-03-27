import logging
from datetime import datetime

logger = logging.getLogger('bookstore')


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path} at {datetime.now()}")
        response = self.get_response(request)
        logger.info(f"Response status: {response.status_code}")
        return response