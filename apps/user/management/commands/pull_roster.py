from django.core.management.base import BaseCommand

from ...models import User
from ...update import update_roster


class Command(BaseCommand):
    help = 'Pulls controller roster from VATUSA API'

    def handle(self, *args, **kwargs):
        update_roster()
        self.stdout.write(f'{User.objects.all().count()} controllers pulled from VATUSA API')
