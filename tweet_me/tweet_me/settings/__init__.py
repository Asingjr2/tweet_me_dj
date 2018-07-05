""" Importing information from other variations of settings"""
from .base import *
from .prod import *
try:
    from .local import *
except: 
    pass