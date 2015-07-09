from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


UserModel = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Stream(models.Model):
  class Meta:
    abstract = True
    managed = False
    
  @classmethod
  def create_stream(cls):
    pass

  @classmethod
  def stream_exists(cls):
    pass


class ContinuousView(models.Model):
  class Meta:
    abstract = True
    managed = False
    
  @classmethod
  def query(cls):
    raise NotImplemented

  @classmethod
  def create_view(cls):
    stmt = 'CREATE CONTINUOUS VIEW %s AS %s' % (cls._meta.db_table,
                                                cls.query())
    # TODO(usmanm): execute stmt

  @classmethod
  def view_exists(cls):
    pass


# We mark all streams and continuous views as non-managed, so that Django
# doesn't try to create migration files for them. To create the stream and
# continuous view call .create_stream() or .create_view() on the class.
class RequestEvent(Stream):
  """
  """
  class Meta:
    managed = False

  scheme = models.TextField()
  method = models.TextField()
  path = models.URLField()
  user = models.ForeignKey(UserModel)
  ip = models.GenericIPAddressField()
  start_time = models.TimeField()
  end_time = models.TimeField()
  success = models.BooleanField()
  status_code = models.IntegerField()
  err_name = models.TextField()


class RequestStats(ContinuousView):
  class Meta:
    managed = False

  path = models.URLField()
  hour = models.DateTimeField()
  num_requests = models.IntegerField()
  num_failures = models.IntegerField()
  unique_users = models.IntegerField()
  unique_ips = models.IntegerField()
  # Our view script creates a field that stores 7 different percentiles:
  #  [1, 5, 10, 50, 90, 95, 99]
  p_latencies = ArrayField(models.FloatField(), size=7) 


class ModelEvent(Stream):
  class Meta:
    managed = False

  type = models.CharField(choices=(('A', 'Added'),
                                   ('D', 'Deleted'),
                                   ('U', 'Updated')))
  name = models.TextField()
  time = models.DateTimeField()


class ModelStats(ContinuousView):
  class Meta:
    managed = False

  name = models.TextField()
  hour = models.DateField()
  num_added = models.IntegerField()
  num_updated = models.IntegerField()
  num_deleted = models.IntegerField()
