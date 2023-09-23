from banking.models import Account
from django.utils import timezone

def disable_updates():
    for a in Account.objects.all():
        a.last_update = timezone.now()
        a.save()