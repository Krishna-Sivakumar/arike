from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction

from care.models import Report, Patient, Treatment
from config import celery_app

from arike.users.models import User

import os

User = get_user_model()


@celery_app.task
def daily_report():
    print("running task...")

    start = datetime.now() - timedelta(days=1)

    report_set = Report.objects.select_for_update().filter(
        last_updated__lte=start,
        disabled=False
    )

    def assemble_report(user: User):
        return f"""
{user}, here's your daily status report:
Patient(s) handled: {Patient.objects.filter(facility = user.facility).count()}

Treatment(s) Done:
{os.linesep.join([f"[{treatment.created_at}] {treatment.care_type}: {treatment.description} " for treatment in Treatment.objects.filter(nurse = user, deleted=False)])}
"""

    with transaction.atomic():
        for report in report_set:
            send_mail(
                subject="Daily Status Report",
                message=assemble_report(report.user),
                from_email="noreply@arike.com",
                recipient_list=[report.user.email, "dummy@user.com"]
            )

            report.last_updated = datetime.now().replace(
                hour=report.time.hour, second=report.time.second)
            report.save()
