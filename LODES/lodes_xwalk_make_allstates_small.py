##############################################################################################

# Script to put all state xwalk_small files together in one document. 
# block-id, blockgroup-id, tract_id

#Created by Maarten on 04/10/2017

##############################################################################################

############################
#0. Setup environment
############################
import pandas as pd

############################
#1. Read in Lodes xwalk files and paste to masterdocument
############################

statename_list=['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id',
				'il','in','ks','ky','la','ma','md','me','mi','mn','mo','ms','mt','nc','nd',
				'ne','nh','nj','nm','nv','ny','oh','ok','or','pa','pr','ri','sc','sd','tn',
				'tx','ut','va','vi','vt','wa','wi','wv','wy']
				


#len(statename_list) moet 53 zijn..

states_processed=0
foldername='/Users/maarten/Desktop/nyu-data/LODES/xwalk/small/'
extension='_xwalk_small.csv'   # remark that we use small here to save space. 

for statename in statename_list:

	print 'Starting treatment of state: ' + str(statename)

	#statename= statename
	filename=statename+extension
	inputfile=foldername+filename
	#print inputfile_xwalk

	# Read in xwalk files
	# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
	dtype_dict={'tabblk2010': object,'trct': object,'bgrp': object}
	df_state_xwalk_small = pd.read_csv(inputfile,
		sep=',', 
		lineterminator='\n', 
		dtype=dtype_dict)
	#names = ["tabblk2010","trct","bgrp"]

	#Append to masterdf
	if states_processed == 0: 
		print 'This is the first state: ' + str(statename)
		states_processed=states_processed+1
		df_master=df_state_xwalk_small
		print 'resulting shape: ' +str(df_master.shape)

	else:
		print 'We are adding the xwalk_small of state: ' + str(statename)
		df_master= df_master.append(df_state_xwalk_small, ignore_index=True)
		states_processed=states_processed+1
		print 'appending shape: ' +str(df_state_xwalk_small.shape)
		print 'resulting shape: ' +str(df_master.shape)



print 'We processed a total of ' + str(states_processed) + ' states'
print 'Starting flushing df_master'
name='all_states_xwalk_small.gzip'
output_name = foldername+name

df_master.to_csv(output_name,sep=',',index=False,compression='gzip')
print  'Ended flushing df_master'

