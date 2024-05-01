from django.utils.deprecation import MiddlewareMixin
from .models import PAGE_VIEW_V2

class PageViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the requested path
        path = request.path

        # Check if the path already exists in the database
        try:
            page_view = PAGE_VIEW_V2.objects.get(path=path)
            # If the path exists, increment the view count
            page_view.views += 1
            page_view.save()
        except PAGE_VIEW_V2.DoesNotExist:
            # If the path doesn't exist, create a new record with a view count of 1
            PAGE_VIEW_V2.objects.create(path=path, views=1)