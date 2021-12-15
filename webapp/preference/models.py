import mongoengine
from webapp.settings import DATABASES
from datetime import datetime

# Connect to Mongodb
mongoengine.connect(DATABASES['default']['NAME'])


class Preference(mongoengine.Document):
    username = mongoengine.StringField()
    close_when_rainy = mongoengine.BooleanField(default=True)
    close_when_dry = mongoengine.BooleanField(default=True)
    temp_max = mongoengine.FloatField(default=35)
    temp_min = mongoengine.FloatField(default=10)
    close_when_windy = mongoengine.BooleanField(default=True)
    diff_temp = mongoengine.IntField(default=2)
    diff_hum = mongoengine.IntField(default=5)
