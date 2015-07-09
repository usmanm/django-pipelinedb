from django.core.exceptions import MiddlewareNotUsed


class RequestLoggingMiddleware(object):
  def __init__(self):
    raise MiddlewareNotUsed

  def process_request(self, request):
    return request

  def process_view(self, request, callback, callback_args, callback_kwargs):
    return None

  def process_template_response(self, request, response):
    return response

  def process_response(self, request, response):
    return response

  def process_exception(self, request, exception):
    return None
