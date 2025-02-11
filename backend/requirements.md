Integrating Swagger into a Django project

>> pip install drf-yasg

Add to installed apps in settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_yasg',
]


The __init__.py files are required in each folder (egrid and r_api) for Python to recognize them as packages.