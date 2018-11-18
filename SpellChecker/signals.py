import logging

from django.contrib.auth.signals import user_logged_out, user_logged_in, user_login_failed
from django.dispatch import receiver
from services import TelemetryFactory

logging.basicConfig(level=logging.INFO)
logger = TelemetryFactory.create(__name__)

