# Administrator Documentation

## Introduction

Welcome to the Cloud VCL Administrator's guide. It will help you set up Cloud VCL
for use by instructors and students. and manage users and functions.

The Cloud VCL application is a Django project. It may be helpful to refer to the official
Django documentation on [deploying Django apps](https://docs.djangoproject.com/en/1.11/howto/deployment/).


## Prerequisites

The Cloud VCL requires access to an OpenStack Cloud project. It may be private or public cloud
and you need to have Tenant ID, Username and Password ready.

Besides this you must have SSL certificate and a (sub)domain name.

To utilize Shibboleth you must be a registered service provider (SP)
recognized by your Shibboleth identity provider (IdP), meaning you
exchanged Metadata before. Refer to [mod_shib](https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPApacheConfig) and shibd daemon documentation.


## Setup

1. Install `pip -r requirements.txt`
1. Customize `settings.py` by putting changes into `local_settings.py` (you will need to create it)
1. Run `python manage.py collectstatic`
1. Run `python manage.py syncimages`
1. Run `python manage.py syncflavors`
1. Add `python manage.py cleanenvironments` as a cron job, run as frequently as necessary

### Integration with Shibboleth

 Cloud VCl is usable with any authentication plugin type that interacts with Apache. only supports Shibboleth and needs to be set up at /Shibboleth.sso

Before you begin it is recommended you complete the following steps:
1. an SSL certificate that you'll use to secure your IdP's browser-facing HTTP connection
2. a source of SAML Metadata for the service providers your IdP will communicate with (this could come from a Federation you've joined, directly from the SP owners, or created and maintained by hand)
3. If you would like to test Cloud VCL for yourself for trial purposes, you can use the [TestShib](http://www.testshib.org/) site 

Next you will need to install Shibboleth SP.


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
Email address: admin@example.com
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
 
 
### Adding/modifying flavors,images and quotas

The admin panel will give you the ability to select and set flavors, images and quotas.

Flavors are accessed via login into the admin panel and selecting 'Flavors' in Site Administration.
Here you will see a list of all flavors available with the ability to filter and organize by column.
To modify a flavor, click on the ID number and you will be able to edit the flavor.
To add a flavor, click the 'Add Flavor' button located on the top right corner of the Flavor administration page.

Images are also accessed via admin panel and selecting 'Images' in Site Administration.
Here you will see a list of all images available with the ability to filter and organize by column.
To modify a image, click on the ID number and you will be able to edit the image.
To add a image, click the 'Add Flavor' button located on the top right corner of the Image administration page.

Quotas are also accessed via admin panel and selecting 'Users' in Site Administration.
Here you will see a list of all users available with the ability to filter and organize by column.
To edit a quota, select the instructor user you wish to change by clicking on their username. Scroll down till the
'Instructor Data' section and edit the values.

### Blocking access to Cloud VCL for specific users
Select 'Users' in Site Administration. To block, select the user by clicking on their username. Scroll down till the
Permissions section and un-check the 'Active' checkbox.

### Finding instance/user by IP

You can find IP Owner History by navigating to:
```
Home/Cvcl/IP Owner History
```
Once at that path, select the username of the user or IP address that you wish to track.
