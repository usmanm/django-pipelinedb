from django.test import TestCase


class TestMiddleware(TestCase):
  def test_dummy(self):
    import time
    time.sleep(10)
