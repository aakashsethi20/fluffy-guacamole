from rest_framework.views import exception_handler

def core_exception_handler(exc, context):

    # If we don't handle the exception then we will pass it to the default 
    # exception handler but even if we do handle it, we still want the 
    # response from DRF.
    response = exception_handler(exc, context)
    
    # adding ValidationError to the handlers to be handled by us
    handlers = {
        'ValidationError': _handle_generic_error,
        'ProfileDoesNotExist': _handle_generic_error,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):
    # just overriding the response data given by DRF and wrapping it under 'errors' key
    response.data = {
        'errors': response.data
    }

    return response