import logging
import time

logger = logging.getLogger('project_logger')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', '')
        method = request.method
        path = request.path
        logger.info(f"Request: {method} {path} from {ip}")

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time()-start_time

        logger.info(f'Response: {method} {path}: {response.status_code} (took {duration:.2f} seconds)')

        return response

