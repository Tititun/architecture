"""This module contains page controllers"""
from jinja2 import Template
import os

def render(template_name, error=None, **kwargs):
    """
    :param template_name: template's name
    :param kwargs: template's parameters
    :return:
    """
    template_path = os.path.join('templates', template_name)
    with open(template_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(error=error, **kwargs)
