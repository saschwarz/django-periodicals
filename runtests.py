import os
import sys
from optparse import OptionParser

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="periodicals.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "haystack",
            "tagging",
            "captcha",
            "periodicals",
        ],
        SITE_ID=1,
        RECAPTCHA_PUBLIC_KEY='public',
        RECAPTCHA_PRIVATE_KEY='private',
        HAYSTACK_CONNECTIONS = {
            'default': {
                'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
                'PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_whoosh_periodicals_index'),
                'STORAGE': 'file',
                'POST_LIMIT': 128 * 1024 * 1024,
                'INCLUDE_SPELLING': True,
                'BATCH_SIZE': 100,
                },
            },
        NOSE_ARGS=['-s'],
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
