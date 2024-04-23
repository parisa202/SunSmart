from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

class PageViewCounterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Increment view count only for the specified URL patterns
        if request.path_info in settings.VIEW_COUNT_URL_PATTERNS:
            view_count_key = f"page_view_count:{request.path_info}"
            view_count = cache.get(view_count_key, 0)
            view_count += 1
            cache.set(view_count_key, view_count)