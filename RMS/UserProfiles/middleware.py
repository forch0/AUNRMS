# # middleware.py

# from django.http import HttpResponseForbidden
# from django.utils.deprecation import MiddlewareMixin

# from django_ratelimit.decorators import ratelimit


# class AdminRateLimitMiddleware(MiddlewareMixin):
    
#     @ratelimit(key='user_or_ip', rate='5/m', method='POST', block=False)
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Check if the request is going to the admin interface
#         if request.path.startswith('/admin/') and request.method == 'POST':
#             # Check if the request is rate-limited
#             if getattr(request, 'limited', False):
#                 return HttpResponseForbidden("You have exceeded the request limit.")
        
#         return None  # Continue processing the request as normal
