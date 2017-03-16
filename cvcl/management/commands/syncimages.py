from django.core.management.base import BaseCommand
from cvcl.models import Image
from cvcl import osapi


class Command(BaseCommand):
    help = 'Imports and updates images from OpenStack'

    def handle(self, *args, **options):
        # connecting to OpenStack API
        conn = osapi.os_connect()
        os_images = list(conn.image.images())
        for os_image in os_images:
            image, created = Image.objects.get_or_create(uuid=os_image.id)
            image.name = os_image.name
            image.size = os_image.size
            image.min_ram = os_image.min_ram
            image.min_disk = os_image.min_disk
            image.save()
            self.stdout.write(self.style.SUCCESS('Successfully saved/updated image "%s"' % image))

        for image in Image.objects.all():
            if not any(x.id == image.uuid for x in os_images):
                image.delete()
                self.stdout.write(self.style.SUCCESS('Deleted removed image "%s"' % image))
