# run_daphne.py
# run_daphne.py
import os
from daphne.cli import CommandLineInterface

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatproject.settings")

# Run Daphne ASGI server (NO 'daphne' in the list)
CommandLineInterface().run([
    "-p", "8000",
    "chatproject.asgi:application"
])
