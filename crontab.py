
from django.core.management import setup_environ

from mixkey import settings
from domain.tasks import send_daily

setup_environ(settings)

send_daily()