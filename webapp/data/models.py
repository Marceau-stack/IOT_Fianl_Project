import mongoengine
from webapp.settings import DATABASES
from datetime import datetime

# Connect to Mongodb
mongoengine.connect(DATABASES['default']['NAME'])


# Create your models here.
class Weather(mongoengine.Document):
    timestamp = mongoengine.DateTimeField()
    temp_in = mongoengine.FloatField()
    temp_out = mongoengine.FloatField()
    hum_in = mongoengine.FloatField()
    hum_out = mongoengine.FloatField()
    wind_speed = mongoengine.FloatField()


class History(mongoengine.Document):
    timestamp = mongoengine.DateTimeField()
    status = mongoengine.StringField()
    user = mongoengine.StringField()
    reason = mongoengine.StringField()

