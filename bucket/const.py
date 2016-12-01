import os

AVAILABLE_COMMANDS = [
    'ls',
    'use',
    'up',
    'down',
    'delete',
    'dir',
    'pwd'
]

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
