"""cloudvcl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from cvcl.admin import admin_site
from django.conf import settings
from django.conf.urls.static import static
import django_saml2_auth.views

urlpatterns = [
    # These are the SAML2 related URLs. You can change "^saml2_auth/" regex to
    # any path you want, like "^sso_auth/", "^sso_login/", etc. (required)
    url(r'^saml2_auth/', include('django_saml2_auth.urls')),

    # The following line will replace the default user login with SAML2 (optional)
    url(r'^accounts/login/$', django_saml2_auth.views.signin),

    url(r'^admin/', admin_site.urls),
    url(r'', include('cvcl.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
