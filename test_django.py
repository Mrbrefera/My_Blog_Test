import django
from django.conf import settings

if not settings.configured:
    print("Django n'est pas configuré correctement.")
else:
    print("Django est configuré correctement.")