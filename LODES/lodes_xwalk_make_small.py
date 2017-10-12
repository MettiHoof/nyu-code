##############################################################################################

#Script to minimize the xwalk data from lodes7 data to the bare minimum to save_space
# block-id, blockgroup-id, tract_id

#Created by Maarten on 04/10/2017

##############################################################################################

############################
#0. Setup environment
############################
import pandas as pd

############################
#1. Read in Lodes xwalk files
############################

#####################
#1.1 Define inputfiles
#####################


statename_list=['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id',
				'il','in','ks','ky','la','ma','md','me','mi','mn','mo','ms','mt','nc','nd',
				'ne','nh','nj','nm','nv','ny','oh','ok','or','pa','pr','ri','sc','sd','tn',
				'tx','ut','va','vi','vt','wa','wi','wv','wy']

#len(statename_list) moet 53 zijn..

for statename in statename_list:

	print 'Starting treatment of state: ' + str(statename)
	foldername_xwalk='/Users/maarten/Desktop/nyu-data/LODES/xwalk/full/'
	statename_xwalk= statename
	extension_xwalk='_xwalk.csv'
	filename_xwalk=statename_xwalk+extension_xwalk

	inputfile_xwalk=foldername_xwalk+filename_xwalk
	#print inputfile_xwalk


	#####################
	#1.2 Read in xwalk files
	#####################

	# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
	dtype_dict={'tabblk2010': object,'trct': object,'bgrp': object}
	df_xwalk = pd.read_csv(inputfile_xwalk,
		sep=',', 
		lineterminator='\n',
		dtype=dtype_dict)
	#names = ["tabblk2010","st","stusps","stname","cty","ctyname","trct","trctname","bgrp","bgrpname","cbsa","cbsaname","zcta","zctaname","stplc","stplcname","ctycsub","ctycsubname","stcd115","stcd115name","stsldl","stsldlname","stsldu","stslduname","stschool","stschoolname","stsecon","stseconname","trib","tribname","tsub","tsubname","stanrc","stanrcname","necta","nectaname","mil","milname","stwib","stwibname","blklatdd","blklondd","createdate"]

	#print df_xwalk.head(10)

	df_xwalk_small=df_xwalk[['tabblk2010','trct','bgrp']]
	#print df_xwalk_small.head(10)

	print 'Ended minimizing xwalk file for state: ' + str(statename)


	############################
	#2. Flushing small xwalkfiles
	############################

	print 'Starting flushing mimized xwalk file for state: ' + str(statename)
	foldername_xwalk_small='/Users/maarten/Desktop/nyu-data/LODES/xwalk/small/'
	newextension='_xwalk_small.csv'
	output_name = foldername_xwalk_small+statename_xwalk+newextension 

	df_xwalk_small.to_csv(output_name,sep=',',index=False)
	print  'Ended flushing mimized xwalk file for state: ' + str(statename)

