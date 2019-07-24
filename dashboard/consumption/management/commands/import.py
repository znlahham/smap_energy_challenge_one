from django.core.management.base import BaseCommand
import os,sys
from datetime import datetime
from consumption.models import UserConsumption,UserData
import time
from enum import Enum


BATCH_NUMBER_TO_INSERT = 500
IS_DEBUG_NUMBER_OF_USERS = 15
IS_DEBUG_NUMBER_OF_CONSUMP = 30



class LoggingType(Enum):
    DEBUG= 1
    WARNING = 2
    ERROR = 3

        





def writelogs(type,val):
	f = open("app_log.txt", "a")
	f.write(datetime.now().strftime("%H:%M:%S.%f;%d/%m/%Y"))
	f.write(";")
	if type == LoggingType.DEBUG:
			f.write("DEBUG;" + str(val))
	elif type == LoggingType.WARNING:
			f.write("WARNING;" + str(val))
	elif type == LoggingType.ERROR:
			f.write("ERROR;" + str(val))
	elif type == LoggingType.INFO:
			f.write("INFO;" + str(val))
	
	f.write('\n')
	f.close()




class Command(BaseCommand):
	help = 'import data'
	def add_arguments(self,parser):
		#adding command to import file.
		#argument -ud: in order to input the userdata csv file
		parser.add_argument('-ud','--user-data',dest= 'get_user_data_csv',help='Imports CSV data of users')
		#argument -cd: in order to input the user consumption csv file.
		parser.add_argument('-cd','--consumption-data',dest= 'get_user_comsp_folder',help='Gets comsumption data file of user')
		#use debug in order to test the overall system.
		parser.add_argument('-debug','--debug',dest= 'debug_mode',help='Sets script in debug mode')
		
	#handling the options to make sure that all the arguments were properly set.
	def handle(self, *args, **options):
		if options['get_user_data_csv'] and options['get_user_comsp_folder'] and options['debug_mode']:
			get_user_data(options['get_user_data_csv'],options['get_user_comsp_folder'],options['debug_mode'])
		else:
			writelogs(LoggingType.ERROR,"Missing Input! Data path or consumption folder")
			#break


			
#used in order to bulk create to sql, this is to avoid hitting the db on each iteration
def bulk_insert_users_data(user_consmuption_list, is_userdata):
	index = 1
	total_inserted_comsumption_data = 0
	range_from = (index - 1) * BATCH_NUMBER_TO_INSERT
	range_to = (index) * BATCH_NUMBER_TO_INSERT
	users_to_import = user_consmuption_list[range_from:range_to]
	while(len(users_to_import) > 0):
		if is_userdata:
			UserData.objects.bulk_create(users_to_import)
		else:
			UserConsumption.objects.bulk_create(users_to_import)
			
		index += 1
		range_from = (index - 1) * BATCH_NUMBER_TO_INSERT
		range_to = (index) * BATCH_NUMBER_TO_INSERT
		users_to_import = user_consmuption_list[range_from:range_to]
		
		
#used to console print the progress bar of the import progress.
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()
	
#get the related data to users and users' consumption.
def get_user_data(user_data_path_csv,user_consumption_path_folder,debug_mode):
	if int(debug_mode ) == 1:
		print ("writing logs")
		writelogs(LoggingType.DEBUG,"deleting database tables")

		
	#truncate tables using models object.
	UserData.objects.all().delete()
	UserConsumption.objects.all().delete()
	#end of truncate
	
	
	temp_users=open(user_data_path_csv ,"r")
	if int(debug_mode ) == 1:
		writelogs(LoggingType.DEBUG,"get UsersData csv file information ")
		writelogs(LoggingType.DEBUG,"getting " + str(IS_DEBUG_NUMBER_OF_USERS) + " of users")
		writelogs(LoggingType.DEBUG,"getting " + str(IS_DEBUG_NUMBER_OF_CONSUMP) + " of consumption per user")
	lines=temp_users.readlines()
	user_data_list=[]
	line_cnt = len(lines)
	printProgressBar(0, line_cnt, prefix = 'Progress:', suffix = 'Complete', length = 50)
	
	for i, l in enumerate(range(1,len(lines))):
		time.sleep(0.1)
		printProgressBar(i + 1, line_cnt, prefix = 'Progress:', suffix = 'Complete', length = 50)
		total_user_consump = 0
		avg_user_consump = 0
		if int(debug_mode) == 1:
			if i == IS_DEBUG_NUMBER_OF_USERS:
				break
		try:
			line = lines[l]
			line_list = line.split(",")
			if len(line_list) == 3:
				user_id = int(line_list[0])
				user_area_temp = line_list[1]
				user_tariff_temp = line_list[2]
				user_consump_path = os.path.join(user_consumption_path_folder ,str(user_id) +".csv")
				if os.path.exists(user_consump_path):
					temp_users_consump=open(user_consump_path ,"r")
					comsumption_data_list = []
					lines_consump = temp_users_consump.readlines()
					for j, l_c in enumerate(range(1,len(lines_consump))):
						if int(debug_mode) == 1:
							if j == IS_DEBUG_NUMBER_OF_CONSUMP:
								break
						try:
							line_consump = lines_consump[l_c]
							user_consump = line_consump.split(",")
							if len(user_consump) == 2:
								consumption_date_time = datetime.strptime(user_consump[0],'%Y-%m-%d %H:%M:%S')
								consumption_val = float(user_consump[1])
								comsumption_data_list.append(UserConsumption(user_id=user_id,date_time=consumption_date_time,comsump_data=consumption_val))
								total_user_consump += consumption_val
								
							else:
								writelogs(LoggingType.WARNING,"skipping consumption line: %s. Wrong data structure" % (j))
						except Exception as e :
							writelogs(LoggingType.WARNING,"error while importing consumption line %s. reason %s:" % (j, e))
					#insert user consumption bulk
					bulk_insert_users_data(comsumption_data_list,False)		
					avg_user_consump = total_user_consump / len(lines_consump)
					avg_user_consump = round(avg_user_consump,3)
					user_data_list.append(UserData(user_id=user_id,user_area=user_area_temp,user_tariff=user_tariff_temp,user_consump_avg =avg_user_consump,user_consump_total=total_user_consump))
				else:
					writelogs(LoggingType.ERROR,"file does not exists")
					
		
			else:
				writelogs(LoggingType.WARNING,"skipping line: %s. Wrong data structure" % (i))

		except Exception as z:
			writelogs(LoggingType.WARNING,"error while importing line %s. reason %s:" % (i,z))
		
	#insert user_data bulk
	bulk_insert_users_data(user_data_list,True)
	writelogs(LoggingType.DEBUG,"DONE!")

	

