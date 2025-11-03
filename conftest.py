import os
import django


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aldovale.settings")
    django.setup()
