#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import os, sys

from django import template

register = template.Library()

@register.filter
def lower(value, arg):
    label = {
        '1': 'ก',
        '2': 'ข',
        '3': 'ค',
        '4': 'ง',
        '5': 'จ'
    }
    return label[str(arg)]
