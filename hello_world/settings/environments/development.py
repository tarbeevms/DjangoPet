import socket
from typing import TYPE_CHECKING

from hello_world.settings.components import config
from hello_world.settings.components.common import (
    DATABASES,
    INSTALLED_APPS,
    MIDDLEWARE,
)

if TYPE_CHECKING:
    from django.http import HttpRequest

# Setting the development status:
DEBUG = True

ALLOWED_HOSTS = [
    config('DOMAIN_NAME'),
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
]


# Application definition

INSTALLED_APPS += (
    # Better debug:
    'debug_toolbar',

    # Linting migrations:
    'django_migration_linter',

    # django-test-migrations:
    'django_test_migrations.contrib.django_checks.AutoNames',
    'django_test_migrations.contrib.django_checks.DatabaseConfiguration',

    # django-extra-checks:
    'extra_checks',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{0}.1'.format(ip[:ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']


def _custom_show_toolbar(request: 'HttpRequest') -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':
        'hello_world.settings.environments.development._custom_show_toolbar',
}

EXTRA_CHECKS = {
    'checks': [
        # Forbid `unique_together`:
        'no-unique-together',
        # Use the indexes option instead:
        'no-index-together',
        # Each model must be registered in admin:
        'model-admin',
        # FileField/ImageField must have non-empty `upload_to` argument:
        'field-file-upload-to',
        # Text fields shouldn't use `null=True`:
        'field-text-null',
        # Don't pass `null=False` to model fields (this is django default)
        'field-null',
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {'id': 'field-foreign-key-db-index', 'when': 'indexes'},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        'field-default-null',
        # Fields with choices must have companion CheckConstraint
        # to enforce choices on database level
        'field-choices-constraint',
    ],
}

# Disable persistent DB connections
DATABASES['default']['CONN_MAX_AGE'] = 0