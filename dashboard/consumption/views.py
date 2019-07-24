# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
from consumption.models import UserConsumption,UserData
from django.db.models import Sum
# Create your views here.


def summary(request):
	#did not use any request data from the url itself



	#get all users_data from UserData model from SQL using Django comamnds.
    users_data = UserData.objects.all().order_by('user_id')

	#get sum of the comsumption with respect to the datetime field
    user_consumps = UserConsumption.objects.values('date_time').annotate(total_consump = Sum('comsump_data'))

	#get all sum to each datetime
    comsumpdata = [[datetime.strftime(user_consump.get('date_time'),"   %m/%d %H:%M:%S"),user_consump.get('total_consump')] for user_consump in user_consumps]
	
	#pass them to the html summary bu the context
    context = {'users_data': users_data, 'users_comsump': comsumpdata}
	
    

	#return needed context to summary.html
    return render(request, 'consumption/summary.html', context)


def detail(request):


	#get user id from request (i.e. from the url itself)
    user_id = request.GET.get('user_id')

	
	#get all user data by filtering using Django on the userid and get only first.
    user_data = UserData.objects.filter(user_id=user_id).first()
	
	#get all user details related to the userID retreived from the url itself.
    user_detail = UserConsumption.objects.filter(user_id=user_id).all()

	
	
	#pass it through the context of the url.
    context = {
            'user_data': user_data,
            'user_detail': user_detail
    }

    return render(request, 'consumption/detail.html', context)
