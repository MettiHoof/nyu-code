##############################################################################################

#Script to aggregate the OD main data from Lodes7 2015 files data. 
#We will aggregate OD matrices from census block to census tracts or blockgroup or whatever is wanted
#Created by Maarten on 03/10/2017

#Remark that the difference between main and aux is that for main we can use the xwalk files 
#for each separate state, making it a smaller join. For aux we need to join with the xwalk 
#file for allstates, which makes up for u huge join. We do both in seperate scripts

##############################################################################################

############################
#0. Setup environment
############################
import pandas as pd


agg_level_list = ['bgrp','trct'] # We will perform aggregation for two levels. 
#'trct'
#'bgrp'


statename_list=['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id',
				'il','in','ks','ky','la','ma','md','me','mi','mn','mo','ms','mt','nc','nd',
				'ne','nh','nj','nm','nv','ny','oh','ok','or','pa','ri','sc','sd','tn',
				'tx','ut','va','vt','wa','wi','wv','wy']

			# Remark, we have 51 states only. pr and vi do not have OD data available
			# WY only has data for 2013 (all the rest is 2015)				


############################
#1. Read in Lodes OD files
############################

#####################
#1.1 Define inputfiles locations
#####################
counter=0

for statename in statename_list:
	counter=counter+1
	print 'State ' + str(counter) + '/51'

	filename='/Users/maarten/Desktop/nyu-data/LODES/OD/main_JT00_2015_source/%s_od_main_JT00_2015.csv.gz' %statename
	if statename=='wy':
		filename='/Users/maarten/Desktop/nyu-data/LODES/OD/main_JT00_2015_source/%s_od_main_JT00_2013.csv.gz' %statename
		# WY only has data for 2013 (all the rest is 2015)	

	filename_xwalk='/Users/maarten/Desktop/nyu-data/LODES/xwalk/small/%s_xwalk_small.csv' %statename

	print 'Started reading in OD data for state ' + str(statename)	
	# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
	dtype_dict={'w_geocode': object,'h_geocode': object}
	df_od = pd.read_csv(filename,sep=',', lineterminator='\n',compression='gzip',dtype=dtype_dict)
	print 'Ended reading in OD data for state ' + str(statename)	

	#names = ["w_geocode","h_geocode","S000","SA01","SA02","SA03","SE01","SE02","SE03","SI01","SI02","SI03","createdate"]
	# 1 	w_geocode	Char15	Workplace Census Block Code
	# 2 	h_geocode 	Char15	Residence Census Block Code
	# 3 	S000		number 	Total number of jobs
	# 4 	SA01 		Num 	Number of jobs of workers age 29 or younger12
	# 5 	SA02 		Num 	Number of jobs for workers age 30 to 5412
	# 6 	SA03 		Num 	Number of jobs for workers age 55 or older12
	# 7 	SE01 		Num 	Number of jobs with earnings $1250/month or less
	# 8 	SE02 		Num 	Number of jobs with earnings $1251/month to $3333/month
	# 9 	SE03 		Num 	Number of jobs with earnings greater than $3333/month
	# 10 	SI01 		Number 	Number of jobs in Goods Producing industry sectors
	# 11 	SI02 		Num 	Number of jobs in Trade, Transportation, and Utilities industry sectors
	# 12 	SI03 		Num 	Number of jobs in All Other Services industry sectors
	# 13 	createdate 	Char 	Date on which data was created, formatted as YYYYMMDD

	print 'Started reading in xwalk data for state ' + str(statename)
	# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
	dtype_dict_xwalk={'tabblk2010': object,'trct': object,'bgrp': object}	
	df_xwalk = pd.read_csv(filename_xwalk,sep=',', lineterminator='\n',dtype=dtype_dict_xwalk)
	df_xwalk_small=df_xwalk[['tabblk2010','trct','bgrp']]
	print 'Ended reading in xwalk data for state ' + str(statename)


	######## Joining 
	print 'Started joining OD and xwalk data'

	df_od_xwalk_tussen=pd.merge(df_od,df_xwalk_small, how='left', left_on='w_geocode', right_on ='tabblk2010')
	df_od_xwalk_tussen=df_od_xwalk_tussen.rename(columns={'trct': 'trct_w','bgrp': 'bgrp_w'})
	df_od_xwalk_tussen=df_od_xwalk_tussen.drop('tabblk2010',1)

	df_od_xwalk=pd.merge(df_od_xwalk_tussen,df_xwalk_small, how='left', left_on='h_geocode', right_on ='tabblk2010')
	df_od_xwalk=df_od_xwalk.rename(columns={'trct': 'trct_h','bgrp': 'bgrp_h'})
	df_od_xwalk=df_od_xwalk.drop('tabblk2010',1)
	df_od_xwalk=df_od_xwalk.drop('createdate',1)
	#print df_od_xwalk.head()

	if len(df_od_xwalk) == len(df_od_xwalk.dropna()):
		print 'Join is ok'
	else:
		print 'Join is not ok, length of tables after join is NOT the same'
	print 'Ended joining OD and xwalk data'


	######## Aggregating
	for agg_level in agg_level_list:

		print 'Started aggregating state ' + str(statename) + ' to aggregation level ' + str(agg_level)

		agg_level_h=agg_level+'_h'
		agg_level_w=agg_level+'_w'

		# make copy so we don't mess with the original data
		df_od_xwalk_copy = df_od_xwalk.copy()
		df_od_agg=df_od_xwalk_copy.groupby([agg_level_w, agg_level_h]).sum().reset_index()
		# Remark that the groupby omits columns that are not numbers. 
		# So no h_geocode, w_geocode(and bgrp_w, bgrp_h for trct level) from df_od_xwalk_copy are preserved after this step
		# https://stackoverflow.com/questions/37575944/pandas-groupby-dropping-columns

		#print df_od_agg.head()
		if len(df_od_xwalk) == len(df_od_agg):
			print 'Aggregating did not have any effect on the lengt of the data, that is not ok'
		else:
			print 'Aggregating has diminished the dataset with ' + str(len(df_od_xwalk)-len(df_od_agg)) + ' lines. To a total of ' + str(len(df_od_agg)) + ' lines.'

		print 'Ended aggregating the data to aggregation level ' + str(agg_level)

		

		######## Flushing
		print 'Started flushing state ' + str(statename) + ' to aggregation level ' + str(agg_level)
		outputname='/Users/maarten/Desktop/nyu-data/LODES/OD/main_JT00_2015_agg_%s/%s_od_main_JT00_2015_agg_%s.csv.gz' %(agg_level,statename, agg_level)

		if statename=='wy':
			outputname='/Users/maarten/Desktop/nyu-data/LODES/OD/main_JT00_2015_agg_%s/%s_od_main_JT00_2013_agg_%s.csv.gz' %(agg_level,statename, agg_level)
			
		df_od_agg.to_csv(outputname,sep=',',index=False,compression='gzip')
		print 'Ended flushing state ' + str(statename) + ' to aggregation level ' + str(agg_level)



