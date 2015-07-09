#!/usr/bin/env python

import django
import sys

from django.test.runner import DiscoverRunner


def run_tests():
  import test_settings

  if hasattr(django, 'setup'):
    django.setup()

  runner = DiscoverRunner(verbosity=1)
  return runner.run_tests(['djpipelinedb'])


def main():
  failures = run_tests()
  sys.exit(failures)


if __name__ == '__main__':
  main()
