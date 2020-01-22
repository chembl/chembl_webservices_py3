import os
import sys
import logging.config


def main():
      os.environ['DJANGO_SETTINGS_MODULE'] = 'chembl_ws_app.settings'

      from django.core.management import execute_from_command_line
      from django.conf import settings

      logging.config.dictConfig(settings.LOGGING)

      execute_from_command_line(sys.argv)


if __name__ == "__main__":
      main()
