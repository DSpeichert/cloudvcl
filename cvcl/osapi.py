from openstack.profile import Profile
from openstack.connection import Connection
from django.conf import settings


def create_connection():
    prof = Profile()
    prof.set_region(Profile.ALL, settings.OS_REGION_NAME)

    return Connection(
        profile=prof,
        user_agent='cloudvcl',
        auth_url=settings.OS_AUTH_URL,
        project_name=settings.OS_PROJECT_NAME,
        username=settings.OS_USERNAME,
        password=settings.OS_PASSWORD,
        user_domain_name='default',
        project_domain_name='default'
    )
