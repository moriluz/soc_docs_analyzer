#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soc_analyzer.settings')
    os.environ.setdefault('OPENAI_API_KEY', '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')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
