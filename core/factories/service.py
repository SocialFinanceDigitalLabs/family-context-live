from datetime import datetime
from random import randint

from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware

from core.models import ServiceSummary


def create_services():
    services = [
        {"id": 1, "title": "Housing", "source": "Housing Database"},
        {"id": 2, "title": "School", "source": "Synergy"},
        {"id": 3, "title": "Adult Social Care", "source": "Liquid Logic"},
        {"id": 4, "title": "Police", "source": "Police Database"},
    ]

    for service in services:
        update_date = datetime.now() - relativedelta(months=randint(1, 8))
        s = ServiceSummary(
            title=service["title"],
            last_synchronised=make_aware(update_date),
            coverage_start_date=update_date - relativedelta(years=3),
            coverage_end_date=update_date - relativedelta(days=7),
            data_source=service["source"],
            records_available=True,
            coverage_explanation="",
            other={},
        )
        s.save()
