from django.conf import settings
from .models import Category

def global_context_renderer(request):
    return {
        'categories': Category.objects.filter(is_active=True),
        'site_name': settings.SITE_NAME,
        'page_title': 'Store',
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION, 
    }