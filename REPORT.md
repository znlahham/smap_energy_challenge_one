SMAP Python Developer Challenge
====


Full Stack Challenge
=====================

How to run the script:
-------------------------


using python 3.6

python manage.py import -ud \user_data.csv -cd \consumption -debug 0 (if debug mode is disabled)
python manage.py import -ud \user_data.csv -cd \consumption -debug 1 (if debug mode is enabled)

Before we start:
-----------------


1- Create models that are essentially our tables that will be used to import data.
2- python import manage.py makemigrations (this is used to migrate the models to become tables in the database).
3- python import manage.py migrate which is used to create/update the table based on the aforementioned migrations).

Unhandled mishaps that might happen:
--------------------------------------

1- if the script runs multiple times, there is no handling on the update on the database.
   (reason for not adding update is due to the fact that the process of not having duplicates, I assume, should not be handled in this script).
   
2- When running the code, the logs of the application are saved in "smap-coding-challenge-master\smap-coding-challenge-master\dashboard\app_log.txt"
   (reason for not using logging library from python is that i was not able to write the debug logging and show them into the file)
   
3- Use datetime as string in html.
   
 
   
   
How to start with the application:
---------------------------------------


1- Pass three arguments:
	- UserData csv file
	- User Consumptions folder
	- Debug mode: 
		* (1) if debug mode is enabled.
		* (0) if debug mode is disabled.
		
		
		
Things done to test the application:
--------------------------------------


1- Add three fields that are active when debug_mode is set to 1.
	- BATCH_NUMBER_TO_INSERT = x
	// this includes the number of records in each bulk to insert x number of transaction to avoid hitting the db on each iteration.
	- IS_DEBUG_NUMBER_OF_USERS = y
	//if debug mode is enabled, we only get y users from the csv file.
	- IS_DEBUG_NUMBER_OF_CONSUMP = z
	// if debug mode is enabled, we only get z transactions for each user.
	
	
Data Handling and Viewing:
----------------------------


We can use Django by objects or by using the following:  EX: UserConsumption.objects.raw('SELECT * FROM myapp_person')
														

1- Have the 2 defs for the 2 html pages for the application: summary.html and details.html
2- send to the context of the html into the views.py in order for them to be used in viewing in html.
3- to show the details view, we pass the user id in order to filter in the usersData table using the html request using the following command:
	- user_id = request.GET.get('user_id')
	
	
4- Add href to the button using the following :"href="/detail?user_id={{o.user_id}}">View Details</a></td>" this will enable us to capture the user id in the details view.

Machine learning part:(not yet implemented).
-----------------------------------------------


After the preprocessing stage of linearizing and normalizing data; the data then is ready to be implemented in our machine learning model.

Algorithm to use is the Extreme Learning Model.

The ELM is used widely in various area for classification and regresion and this is due to the fact the ELM learns faster and is very quick.
	
ELM has been widely used for energy consumption prediction.



	
	
	
