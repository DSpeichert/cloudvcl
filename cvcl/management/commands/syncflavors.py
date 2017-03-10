from django.core.management.base import BaseCommand
from cvcl.models import Flavor
from cvcl import osapi


class Command(BaseCommand):
    help = 'Imports and updates flavors from OpenStack'

    def handle(self, *args, **options):
        # connecting to OpenStack API
        conn = osapi.create_connection()
        os_flavors = list(conn.compute.flavors())
        for os_flavor in os_flavors:
            flavor, created = Flavor.objects.get_or_create(uuid=os_flavor.id)
            flavor.name = os_flavor.name
            flavor.save()
            self.stdout.write(self.style.SUCCESS('Successfully saved/updated flavor "%s"' % flavor))

        for flavor in Flavor.objects.all():
            if not any(x.id == flavor.uuid for x in os_flavors):
                flavor.delete()
                self.stdout.write(self.style.SUCCESS('Deleted removed flavor "%s"' % flavor))
