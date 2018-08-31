"""
apps.py
====================================
The core module of my example project
"""
from django.apps import AppConfig

def about_me(your_name):
    """Return the most important thing about a person.
    """
    return "The wise {} loves Python.".format(your_name)

class DqConfig(AppConfig):
    """An example docstring for a class definition."""
    name = 'dq'

