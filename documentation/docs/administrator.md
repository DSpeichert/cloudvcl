# Administrator Documentation

## Introduction

Welcome to the Cloud VCL Administrator's guide. It will help you set up Cloud VCL
for use by instructors and students. and manage users and functions.

The Cloud VCL application is a Django project. It may be helpful to refer to the official
Django documentation on [deploying Django apps](https://docs.djangoproject.com/en/1.11/howto/deployment/).

*To be continued...*

## Prerequisites

The Cloud VCL requires access to an OpenStack Cloud project. It may be private or public cloud
and you need to have Tenant ID, Username and Password ready.

*To be continued...*

## Setup

1. Install `pip -r requirements.txt`
1. Customize `settings.py` by putting changes into `local_settings.py` (you need to create it)
1. Run `python manage.py syncimages`
1. Run `python manage.py syncimages`
1. Add `python manage.py cleanenvironments` as a cron job, as frequently as necessary


### Integration with Shibboleth

*To be continued... (say it currently only supports Shibboleth and need to be set up at /Shibboleth.sso)*

### Superadmin account
To be able to administer the site and login to the admin panel, you must first create a superuser account.
In order to do this go back to the command line and type
```
python manage.py createsuperuser`
```
Press enter, and when prompted, type your username (lowercase, no spaces), email address, and password.
Don't worry that you can't see the password you're typing in – that's how it's supposed to be. Just type
it in and press enter to continue. The output should look like this (where the username and email should
be your own ones):
```
(myvenv) ~/django$ python manage.py createsuperuser
Username: admin
Email address: admin@admin.com
Password:
Password (again):
Superuser created successfully.
```
Return to your browser. Log in with the superuser's credentials you chose; you should see the Django admin
dashboard.

## The Django admin site

One of the most powerful parts of Django is the automatic admin interface. If you want to know more about
Django admin, you should check [Django's Admin documentation](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/).
Once you have logged into the Django Admin panel, you will be able to begin site administration.
Here you can view recent actions that have been performed on the right center of the screen. You can also
drill down by subject area to perform actions. Note that each subject area has the option of `Add` or `Edit` that serves
as a quicklink to the action.
 
 
### Adding/modifying instructors

TODO: how to select flavors, images, quotas

### Blocking access to Cloud VCL for specific users

TODO

### Finding instance/user by IP

TODO
