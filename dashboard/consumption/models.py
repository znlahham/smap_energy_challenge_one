# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


#class of userData; declaring fields
class UserData(models.Model):
	# user_id;integer field
    user_id = models.IntegerField(null=False)
	# user_area;string field
    user_area = models.CharField(max_length=255, null=False)
	# user_tarrif;string field
    user_tariff = models.CharField(max_length=255, null=False)
	# user_consump_avg;double field
    user_consump_avg = models.FloatField(default=0)
	# user_consump_total;double field
    user_consump_total = models.FloatField(default=0)




#class of userConsumption; declaring fields
class UserConsumption(models.Model):
	# user_id;integer field
    user_id = models.IntegerField(null=False)
	# consump_datetime;datetime field
    date_time = models.DateTimeField(null = False)
	# comsump_data;double field
    comsump_data = models.FloatField(null=False)

