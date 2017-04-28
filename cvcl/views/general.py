import logging
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import login, authenticate, get_user_model
from django.core.urlresolvers import get_script_prefix


def index(request):
    return render(request, 'index.html')


def logout(request):
    auth_logout(request)
    return redirect(settings.LOGOUT_URL)


def shib_login(request):
    """Authenticate a session using Shibboleth.
        This allows Shibboleth to be one of many options for authenticating to
        the site. Instead of protecting the whole site via Shibboleth, we protect
        a single view (this view).  The view will authenticate the user using
        the attributes passed in via request.META to authenticate the user.
        Based on code from: https://github.com/esnet/shibboleth_session_auth
        """

    idp_attr = settings.SHIBBOLETH_SESSION_AUTH['IDP_ATTRIBUTE']
    idp = request.META.get(idp_attr)
    if not idp:
        # log
        logging.info("IdP header missing", idp_attr)
        return HttpResponseBadRequest("Invalid response from IdP")

    if idp not in settings.SHIBBOLETH_SESSION_AUTH['AUTHORIZED_IDPS']:
        # log
        logging.info("Unauthorized IdP", idp)
        return HttpResponseForbidden("unauthorized IdP: {}".format(idp))

    user_attrs = {}

    for http_attr, user_attr, required in settings.SHIBBOLETH_SESSION_AUTH['USER_ATTRIBUTES']:
        user_attrs[user_attr] = request.META.get(http_attr, None)
        if required and user_attrs[user_attr] is None:
            # log
            logging.info("SSO missing attribute: {}", user_attr)
            return HttpResponseBadRequest("Invalid response from IdP")

    try:
        user = get_user_model().objects.get(username=user_attrs['username'])
    except get_user_model().DoesNotExist:
        user = get_user_model()(**user_attrs)
        user.set_unusable_password()
        user.save()

    # requires django.contrib.auth.backends.RemoteUserBackend in AUTHENTICATION_BACKENDS
    user = authenticate(remote_user=user.username)
    login(request, user)

    if "next" in request.GET:
        redirect_target = request.GET['next']
    else:
        redirect_target = get_script_prefix()

    return HttpResponseRedirect(redirect_target)
