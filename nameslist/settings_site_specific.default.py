"""
This is a base template for what to put in your settings_site_specific.py
copy this file to settings_site_specific.py and follow the directions herewithin to create a correctly formed settings file
"""

# Use the following code to generate a new secret key
# This is the same code that django uses for this task
#
# from django.utils.crypto import get_random_string
#
# chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# get_random_string(50, chars)

SECRET_KEY = ''

# debug settings follow normal django convention
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []