from rest_framework.views import exception_handler
import traceback

def custom_handler(exc, context):
    resp = exception_handler(exc, context)
    if resp is not None:
        resp.data["status"] = resp.status_code
        resp.data["message"] = ''.join([s + "\n" for s in traceback.format_tb(exc.args[0].__traceback__)]) 
    return resp