# app/context_processors.py
import os
from django.conf import settings

def banner_images(request):
    banner_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images/banner')
    try:
        images = [
            f'images/banner/{f}' 
            for f in os.listdir(banner_dir) 
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ]
    except FileNotFoundError:
        images = []
    return {'banner_images': images}
