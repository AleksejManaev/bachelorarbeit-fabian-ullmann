#!/usr/bin/env python
import sys

import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ba.settings")
    # os.environ["DJANGO_SETTINGS_MODULE"] = "audi_mediamanager.settings_local"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
