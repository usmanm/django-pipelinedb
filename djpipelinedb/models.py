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
  PERCENTILES = [1, 5, 10, 50, 90, 95, 99]

  path = models.URLField()
  hour = models.DateTimeField()
  num_requests = models.IntegerField()
  num_failures = models.IntegerField()
  unique_users = models.IntegerField()
  unique_ips = models.IntegerField()
  # Our view script creates a field that stores 7 different percentiles,
  # see RequestStats.PERCENTILES
  p_latencies = ArrayField(models.FloatField(), size=7) 

  @classmethod
  def query(cls):
    return """
    SELECT
      path::text,
      hour(start_time::timestamptz) AS hour,
      count(*) as num_requests,
      count(*) FILTER (WHERE NOT success::bool) as num_failures,
      count(DISTINCT user::int) AS unique_users,
      count(DISTINCT ip::text) AS unique_ips,
      percentile_cont(ARRAY[%s]) WITHIN GROUP
        (ORDER BY EXTRACT(epoch FROM end_time::timestamptz - start_time))
        AS p_latencies
    FROM %s
    GROUP BY (path, hour)
    """ % (', '.join([str(i) for i in cls.PERCENTILES]),
           RequestEvent._meta.db_table)


class UserEngagementStats(ContinuousView):
  user = models.ForeignKey(UserModel)
  
  

class ModelEvent(Stream):
  type = models.CharField(choices=(('A', 'Added'),
                                   ('U', 'Updated'),
                                   ('D', 'Deleted')))
  name = models.TextField()
  time = models.DateTimeField()


class ModelStats(ContinuousView):
  name = models.TextField()
  hour = models.DateField()
  num_added = models.IntegerField()
  num_updated = models.IntegerField()
  num_deleted = models.IntegerField()

  @classmethod
  def query(cls):
    return """
    SELECT
      name::text,
      hour(start_time::timestamptz) AS hour,
      count(*) FILTER (WHERE type::char = 'A') as num_added,
      count(*) FILTER (WHERE type::char = 'U') as num_updated,
      count(*) FILTER (WHERE type::char = 'D') as num_deleted,
    FROM %s
    GROUP BY (name, hour)
    """ % ModelEvent._meta.db_table
