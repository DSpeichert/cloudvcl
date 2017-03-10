# CloudVCL [![Build Status](https://travis-ci.org/DSpeichert/cloudvcl.svg?branch=master)](https://travis-ci.org/DSpeichert/cloudvcl)
Cloud VCL


How to use/test:

1. Put OS password in `settings.py`
1. Run migrations: `./manage.py migrate`
1. Create admin account: `./manage.py createsuperuser`
1. Sync images: `./manage.py syncimages`
1. Sync flavors: `./manage.py syncflavors`
1. Run server: `./manage.py runserver`