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
1. Run `python manage.py collectstatic`
1. Run `python manage.py syncimages`
1. Run `python manage.py syncflavors`
1. Add `python manage.py cleanenvironments` as a cron job, as frequently as necessary

### Integration with Shibboleth

*To be continued... (say it currently only supports Shibboleth and need to be set up at /Shibboleth.sso)*


Example Apache httpd vhost config file:

```
<VirtualHost *:80>
    ServerName      cloudvcl.example.com
    RedirectMatch permanent ^(?!/\.well-known) https://cloudvcl.example.com/
</VirtualHost>

# https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=apache-2.4.6&openssl=1.0.1e&hsts=yes&profile=modern
SSLProtocol             all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite          ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256
SSLHonorCipherOrder     on
SSLCompression          off


# OCSP Stapling, only in httpd 2.3.3 and later
SSLUseStapling          on
SSLStaplingResponderTimeout 5
SSLStaplingReturnResponderErrors off
SSLStaplingCache        shmcb:/var/run/ocsp(128000)

<VirtualHost *:443>
    ServerName cloudvcl.example.com
    SSLEngine On
    SSLCertificateFile      /etc/letsencrypt/live/cloudvcl.example.com/cert.pem
    SSLCertificateChainFile /etc/letsencrypt/live/cloudvcl.example.com/chain.pem
    SSLCertificateKeyFile   /etc/letsencrypt/live/cloudvcl.example.com/privkey.pem

    Header always set Strict-Transport-Security "max-age=15768000"

    Alias /media/ /home/cloudvcl/cloudvcl/media/
    Alias /static/ /home/cloudvcl/cloudvcl/static/

    <Directory /home/cloudvcl/cloudvcl/static>
        Require all granted
    </Directory>

    <Directory /home/cloudvcl/cloudvcl/media>
        Require all granted
    </Directory>

    WSGIDaemonProcess cloudvcl python-path=/home/cloudvcl/cloudvcl
    WSGIProcessGroup cloudvcl
    WSGIScriptAlias / /home/cloudvcl/cloudvcl/cloudvcl/wsgi.py process-group=cloudvcl

    <Directory /home/cloudvcl/cloudvcl/cloudvcl>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    <Location /Shibboleth.sso>
        SetHandler shib
    </Location>

    <Location /login>
        AuthType shibboleth
        ShibRequestSetting requireSession 1
        Require valid-user
    </Location>
</VirtualHost>
```

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
