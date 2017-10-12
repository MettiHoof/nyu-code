##############################################################################################

#Script to plot the flows in the LODES OD files (both main and aux, agg at blgr and trct)
#Created by Maarten on 05/10/2017

##############################################################################################

############################
#0. Setup environment
############################
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as clr
from matplotlib.collections import LineCollection

#Choose variable from OD file to work with:
variable='S000'

############################
#1. Read in geo_data 
############################

#Remark that the OD data, although captured for 2015 are in census regions of 2010 delineation, as described in their metadata

inputfile_geo_bgrp='/Users/maarten/Desktop/nyu-data/NHGIS/shapefiles/shapefiles_us_in_csv_format/shapefile_us_blockgroup_2010.csv'
# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
dtype_dict_bgrp={'STATEFP10': object,'GEOID10': object}
df_geo_bgrp = pd.read_csv(inputfile_geo_bgrp,sep=',',lineterminator='\n',dtype=dtype_dict_bgrp)
#STATEFP;COUNTYFP;TRACTCE;BLKGRPCE;GEOID;NAMELSAD;MTFCC;FUNCSTAT;ALAND;AWATER;INTPTLAT;INTPTLON;GISJOIN;Shape_Leng;Shape_Area
df_geo_bgrp_small=df_geo_bgrp[['STATEFP10','GEOID10','INTPTLAT10','INTPTLON10']]

inputfile_geo_trct='/Users/maarten/Desktop/nyu-data/NHGIS/shapefiles/shapefiles_us_in_csv_format/shapefile_us_censustract_2010.csv'
#STATEFP,COUNTYFP,TRACTCE,GEOID,NAME,NAMELSAD,MTFCC,FUNCSTAT,ALAND,AWATER,INTPTLAT,INTPTLON,GISJOIN,Shape_Leng,Shape_Area
# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
dtype_dict_trct={'STATEFP10': object,'GEOID10': object}
df_geo_trct = pd.read_csv(inputfile_geo_trct,sep=',',lineterminator='\n',dtype=dtype_dict_trct)
df_geo_trct_small=df_geo_trct[['STATEFP10','GEOID10','INTPTLAT10','INTPTLON10']]


############################
#2. Define helper functions 
############################

def join_geodata (df_od,df_geo,agg_level,variable,variable_min=0) :

	print 'Start joining OD and Geo data'

	#Get variable from df_od on which we need to do the join
	id_h=agg_level+'_h'
	id_w=agg_level+'_w'
	
	df_od_small=df_od[[id_w,id_h,variable]].copy()

	#Get variable from geo file on which we need to do the join is GEOID10 for both agg levels
	id_geo='GEOID10'
	'''
	#deze id-geos zijn niet de volledige identifiers
	if agg_level=='trct':
		id_geo='TRACTCE10'
	elif agg_level=='bgrp':
		id_geo='BLKGRPCE10'
	'''
	
	df_tussen=pd.merge(df_od_small,df_geo,how='left', left_on=id_w, right_on=id_geo)
	df_tussen=df_tussen.rename(columns={'INTPTLAT10': 'lat_w','INTPTLON10': 'lon_w'})
	df_tussen=df_tussen.drop([id_geo,'STATEFP10'],1)
	
	df_od_joined=pd.merge(df_tussen,df_geo,how='left', left_on=id_h, right_on=id_geo)
	df_od_joined=df_od_joined.rename(columns={'INTPTLAT10': 'lat_h','INTPTLON10': 'lon_h'})
	df_od_joined_out=df_od_joined.drop(id_geo,1)
	print 'Ended joining OD and Geo data'

	# Perform filtering as imposed by the variable_min argument
	if variable_min==0:
		print 'we are not performing any filtering'
	else:
		print 'We are performing filtering by the variable_min argument'
		df_od_work=df_od_joined.copy()
		df_od_joined_out=df_od_work.loc[df_od_work[variable]>variable_min]
		print 'Ended filtering by the variable_min argument'

	############################
	## Investigate the NaN's nog, welke joinen lukken niet?
	############################
	
	return df_od_joined_out


def plot_coordinates(df_od,lon_colname,lat_colname):

	#get weird alaskan coordinates out of the way
	df_od_work=df_od.copy()
	df_od_out=df_od_work.loc[(df_od_work[lon_colname]>-150) & (df_od_work[lat_colname]<55)]

	plt.scatter(df_od_out[lon_colname],df_od_out[lat_colname],s=1,alpha=0.5)

	plt.show()
	plt.close('all')

	return 'done'


def plot_flows_state(df_od,lon_h,lat_h,lon_w,lat_w,variable,variable_min,statename,agg_level,cat):

	#take copy and filter on variable_min
	df_od_work=df_od.copy()
	df_od=df_od_work.loc[df_od_work[variable]>variable_min]

	#get weird alaskan coordinates out of the way
	df_od_work=df_od.copy()
	df_od=df_od_work.loc[(df_od_work[lon_h]>-150) & (df_od_work[lat_h]<55) & (df_od_work[lon_w]>-150) & (df_od_work[lat_w]<55) & (df_od_work[lon_w]<-40) & (df_od_work[lon_h]<-40)]

	# Create lines to be drawn
	lines=[]
	#for index, row in df.iterrows(): #Itertuples is faster
	for row in df_od.itertuples():
		line=[(row.lon_h,row.lat_h),(row.lon_w,row.lat_w)]
		#print line
		lines.append(line)

	#Setup input for line collection

	print df_od.head(3)

	lines_array=np.array(lines)
	weight=np.array(df_od[variable])
	weight_max= 500 #weight.max()
	weight_min= variable_min #weight.min()
	#weight_lin_min=weight/weight_min #is an int

	#Setup linecollection

	lc = LineCollection(lines_array, cmap='autumn_r',norm=clr.LogNorm(weight_min,weight_max)) # add _r for reversed colorscheme
	#matplotlib.colors.LogNorm(vmin=None, vmax=None, clip=False)
	#matplotlib.colors.NoNorm(vmin=None, vmax=None, clip=False)
	#matplotlib.colors.Normalize(vmin=None, vmax=None, clip=False)
	#matplotlib.colors.PowerNorm(gamma, vmin=None, vmax=None, clip=False)
	#matplotlib.colors.SymLogNorm(linthresh, linscale=1.0, vmin=None, vmax=None, clip=False)

	lc.set_array(weight)
	lc.set_linewidth(1)
	#lc.set_linewidth(weight_lin_min)
	lc.set_alpha(0.4)

	#Plot
	fig, ax = plt.subplots(figsize=(18,12))
	# This way you only plot the locations of the home census, might be you miss out on some work areas that don't have homes. 
	ax.scatter(df_od[lon_h],df_od[lat_h],s=0.5,alpha=0.8, c='grey')
	ax.add_collection(lc)
	#ax.set_xlim(-74.03,-74.9)
	#ax.set_ylim(-160,-140) 

	# Setup figure
	ax.autoscale_view()
	ax.margins(0.1) # Margins to the side of the figure
	title='Commuting flows for state: %s at %s level' %(statename,agg_level)
	ax.set_title(title)
	ad_text= 'filtered on minimal ' + str(variable_min) + ' for variable ' + str(variable)
	ax.annotate(ad_text, xy=(0.05, 0.94), xycoords='axes fraction')

	#Setup colorbar, needs to have its own axes, so we make sure that axes is where we want it
	left, bottom, width, height = [0.82, 0.13, 0.015, 0.3]
	ax2 = fig.add_axes([left, bottom, width, height])
	axcb=fig.colorbar(lc,cax=ax2)
	label='Number of commuters'
	axcb.set_label(label,rotation=270, va='bottom')

	#Show or flush
	#plt.tight_layout()
	#plt.show()

	
	#outputfolder='/Users/maarten/Desktop/nyu-code/LODES/Figures/maps_lodes_flows_per_state'
	#outputname='map_%s_od_%s_JT00_2015_%s_%s_2015_agg_%s.png' %(statename,cat,statename,agg_level,variable)

	outputfolder='/Users/maarten/Desktop/nyu-code/LODES/Figures/maps_lodes_flows_all_states/'
	outputname='map_allstates_od_%s_JT00_2015_agg_%s_var_%s_var_min_%s_%s-%s.png' %(cat,agg_level,variable,variable_min,weight_min,weight_max)
	output=outputfolder+outputname
	print output	
	plt.savefig(output)
	plt.close("all")

	print 'Finished map for ' + str(statename) +'_' + str(cat) +'_' + str(agg_level) 

	return 'tettn'

############################
#2. Run analysis: read in, join with geo, and plot
############################

############################
#2.1 For one case
############################
'''
agg_level='trct'
statename='al'
cat='main'


#Read in
inputfile='/Users/maarten/Desktop/nyu-data/LODES/OD/%s_JT00_2015_agg_%s/%s_od_%s_JT00_2015_agg_%s.csv.gz' %(cat,agg_level,statename,cat,agg_level)
#if statename=='wy':
	#inputfile='/Users/maarten/Desktop/nyu-data/LODES/OD/%s_JT00_2015_agg_%s/%s_od_%s_JT00_2013_agg_%s.csv.gz' %(cat,agg_level,statename,cat,agg_level)
# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
dtype_dict_od={'trct_w': object,'trct_h': object,'bgrp_w': object,'bgrp_h': object}
df_od = pd.read_csv(inputfile,sep=',', lineterminator='\n',compression='gzip',dtype=dtype_dict_od)
print 'Ended reading in data for state ' + str(statename)


if agg_level=='trct':
	df_geo_copy=df_geo_trct_small.copy()
elif agg_level=='bgrp':
	df_geo_copy=df_geo_bgrp_small.copy()


#Join

id_h=agg_level+'_h'
id_w=agg_level+'_w'
	
df_od_small=df_od[[id_w,id_h,variable]].copy()

#Get variable from geo file on which we need to do the join is GEOID10 for both agg levels
id_geo='GEOID10'

	
df_tussen=pd.merge(df_od_small,df_geo_copy,how='left', left_on=id_w, right_on=id_geo)
df_tussen=df_tussen.rename(columns={'INTPTLAT10': 'lat_w','INTPTLON10': 'lon_w'})
df_tussen=df_tussen.drop([id_geo,'STATEFP10'],1)
	
df_od_joined=pd.merge(df_tussen,df_geo_copy,how='left', left_on=id_h, right_on=id_geo)
df_od_joined=df_od_joined.rename(columns={'INTPTLAT10': 'lat_h','INTPTLON10': 'lon_h'})
df_od_joined=df_od_joined.drop(id_geo,1)

if len(df_od_joined) == len(df_od_joined.dropna()):
	print 'Join is ok'
else:
	print 'Join is not ok, we have ' + str(len(df_od_joined) - len(df_od_joined.dropna())) + ' NaNs'
	## Investigate the NaN's welke joins lukken niet; vaak enkele tractsnummers
	#df_od_joined_nans = df_od_joined[df_od_joined.isnull().any(axis=1)]


df_od_lat_lon=df_od_joined.copy()
#plot_coordinates(df_od_lat_lon,'lon_w','lat_w')

variable_min = 50 
plot_flows_state(df_od_lat_lon,'lon_h','lat_h','lon_w','lat_w',variable,variable_min,statename,agg_level,cat)

'''



############################
#2.2 For all states, seperately.
############################
'''
agg_level_list = ['trct'] # ['bgrp','trct'] # We will perform aggregation for two levels. 


statename_list=['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id',
				'il','in','ks','ky','la','ma','md','me','mi','mn','mo','ms','mt','nc','nd',
				'ne','nh','nj','nm','nv','ny','oh','ok','or','pa','ri','sc','sd','tn',
				'tx','ut','va','vt','wa','wi','wv','wy']
'''
'''
statename_list=['ar','al']
'''
'''
			# Remark, we have 51 states only. pr and vi do not have OD data available
			# WY only has data for 2013 (all the rest is 2015)			

cat_list=  ['main']# ['aux','main'] 
# Categories of OD data. Aux is work within state but home outside. main is both home and work inside state


for agg_level in agg_level_list:
	# Get the right geo_data file
	if agg_level=='trct':
		df_geo_copy=df_geo_trct_small.copy()
	elif agg_level=='bgrp':
		df_geo_copy=df_geo_bgrp_small.copy()

	for statename in statename_list:
		for cat in cat_list:

			#Read in
			print 'Reading in data for state: ' + str(statename)
			inputfile='/Users/maarten/Desktop/nyu-data/LODES/OD/%s_JT00_2015_agg_%s/%s_od_%s_JT00_2015_agg_%s.csv.gz' %(cat,agg_level,statename,cat,agg_level)
			if statename=='wy':
				inputfile='/Users/maarten/Desktop/nyu-data/LODES/OD/%s_JT00_2015_agg_%s/%s_od_%s_JT00_2013_agg_%s.csv.gz' %(cat,agg_level,statename,cat,agg_level)

			# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
			dtype_dict_od={'trct_w': object,'trct_h': object,'bgrp_w': object,'bgrp_h': object}
			df_od = pd.read_csv(inputfile,sep=',', lineterminator='\n',compression='gzip',dtype=dtype_dict_od)
			print 'Ended reading in data for state ' + str(statename)

			#Join
			df_od_lat_lon=join_geodata(df_od,df_geo_copy,agg_level,variable)
			# Maps
			#plot_coordinates(df_od_lat_lon,'lon_w','lat_w')
			variable_min= 10
			plot_flows_state(df_od_lat_lon,'lon_h','lat_h','lon_w','lat_w',variable,variable_min,statename,agg_level,cat)

'''
############################
#2.2 For all states, together
############################

############################
#2.2.1 Create pickle to store all OD's from main and aux, for a given minimum value of S0000
############################

'''
agg_level_list = ['trct'] # ['bgrp','trct'] # We will perform aggregation for two levels. 


statename_list=['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id',
				'il','in','ks','ky','la','ma','md','me','mi','mn','mo','ms','mt','nc','nd',
				'ne','nh','nj','nm','nv','ny','oh','ok','or','pa','ri','sc','sd','tn',
				'tx','ut','va','vt','wa','wi','wv','wy']

			# Remark, we have 51 states only. pr and vi do not have OD data available
			# WY only has data for 2013 (all the rest is 2015)			

cat_list=  ['aux']# ['aux','main'] 
# Categories of OD data. Aux is work within state but home outside. main is both home and work inside state



for agg_level in agg_level_list:
	df_samen=0 # reset df_samen when we change agg_level
	counter=0 # reset counter when we change agg_level

	if agg_level=='trct':
		df_geo_copy=df_geo_trct_small.copy()
	elif agg_level=='bgrp':
		df_geo_copy=df_geo_bgrp_small.copy()

	for cat in cat_list:
		for statename in statename_list:
			counter=counter + 1
			#Read in
			print 'Reading in data for state: ' + str(statename)
			inputfile='/Users/maarten/Desktop/nyu-data/LODES/OD/%s_JT00_2015_agg_%s/%s_od_%s_JT00_2015_agg_%s.csv.gz' %(cat,agg_level,statename,cat,agg_level)
			if statename=='wy':
				inputfile='/Users/maarten/Desktop/nyu-data/LODES/OD/%s_JT00_2015_agg_%s/%s_od_%s_JT00_2013_agg_%s.csv.gz' %(cat,agg_level,statename,cat,agg_level)

			# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
			dtype_dict_od={'trct_w': object,'trct_h': object,'bgrp_w': object,'bgrp_h': object}
			df_od = pd.read_csv(inputfile,sep=',', lineterminator='\n',compression='gzip',dtype=dtype_dict_od)
			print 'Ended reading in data for state ' + str(statename)

			#Join and filter by variable_min argument
			variable_min= 10
			df_od_lat_lon=join_geodata(df_od,df_geo_copy,agg_level,variable,variable_min)
			print df_od_lat_lon.size

			# Merge
			if counter==1:
				df_samen=df_od_lat_lon.copy()
				print 'first one'
				print counter
				print df_samen.size
			else:
				df_samen=df_samen.append(df_od_lat_lon, ignore_index=True)
				print df_samen.size
				print 'second one'
				print counter

		# Save big csv file with all states as pickle (.pkl)
		pickle_folder='/Users/maarten/Desktop/nyu-data/LODES/OD/'
		pickle_file='pickle_allstates_od_%s_JT00_2015_agg_%s_var_%s_var_min_%s.pkl' %(cat,agg_level,variable,variable_min)
		pickle_name= pickle_folder+pickle_file
		df_samen.to_pickle(pickle_name)  # where to save it, usually as a .pkl


# Putting aux and main together
pickle_name_aux= '/Users/maarten/Desktop/nyu-data/LODES/OD/pickle_allstates_od_aux_JT00_2015_agg_trct_var_S000_var_min_10.pkl'
pickle_name_main= '/Users/maarten/Desktop/nyu-data/LODES/OD/pickle_allstates_od_main_JT00_2015_agg_trct_var_S000_var_min_10.pkl'

pickle_name_main_and_aux= '/Users/maarten/Desktop/nyu-data/LODES/OD/pickle_allstates_od_main_and_aux_JT00_2015_agg_trct_var_S000_var_min_10.pkl'

df_aux=pd.read_pickle(pickle_name_aux)
df_main=pd.read_pickle(pickle_name_main)

df_main_and_aux=df_main.append(df_aux, ignore_index=True)

df_main_and_aux.to_pickle(pickle_name_main_and_aux)
'''

############################
#2.2.2 Start mapping based on pickle.
############################

# Load pickle back in:
print 'start reading pickle'	
pickle_name_main_and_aux= '/Users/maarten/Desktop/nyu-data/LODES/OD/pickle_allstates_od_main_and_aux_JT00_2015_agg_trct_var_S000_var_min_10.pkl'

df_maps = pd.read_pickle(pickle_name_main_and_aux)
print 'ended reading pickle'



#Maps
print 'start mapping'
#plot_coordinates(df_maps,'lon_w','lat_w')
agg_level="trct"
cat='main_and_aux'
variable_min= 11
plot_flows_state(df_maps,'lon_h','lat_h','lon_w','lat_w',variable,variable_min,'all_states',agg_level,cat)






############################
#2. Read in lat lon info for census blocks 

##!!!! Opgepast, we hebben de data hier enkel voor New York City county, 
##andere counties moeten apart worden gedownload:

###########################


#####################
#2.1 Define inputfiles
# The NY_36061_NY_blocks_lat_lon was made based on the 2010_NY_36061_NY_blocks_boundary_files shapefile, then in qgis. 
#####################
'''
print 'Reading in geo data'

foldername_geo='/Users/maarten/Desktop/nyu-data/LODES/'
inputname_geo='NY_36061_NY_blocks_lat_lon.csv'

inputfile_geo=foldername_geo + inputname_geo

df_geo = pd.read_csv(inputfile_geo,
	sep=',', 
	lineterminator='\n', 
	header=0,
	names = ['STATEFP10','COUNTYFP10','TRACTCE10','BLOCKCE10','GEOID10','NAME10','MTFCC10','UR10','UACE10','UATYP10','FUNCSTAT10','ALAND10','AWATER10','INTPTLAT10','INTPTLON10']
	)

print df_geo.head(10)
df_geo_small=df_geo[['GEOID10','INTPTLAT10','INTPTLON10']]

print 'Ended reading in geo data'
'''
############################
#3. Join Lodes OD with Lat lon info
############################
'''
print 'Start joining OD and Geo data'

df_od_lat_lon_tussen=pd.merge(df_od_small,df_geo_small, how='left', left_on='w_geocode', right_on ='GEOID10')
df_od_lat_lon_tussen=df_od_lat_lon_tussen.rename(columns={'INTPTLAT10': 'lat_w','INTPTLON10': 'lon_w'})
df_od_lat_lon_tussen=df_od_lat_lon_tussen.drop('GEOID10',1)
df_od_lat_lon=pd.merge(df_od_lat_lon_tussen,df_geo_small, how='left', left_on='h_geocode', right_on ='GEOID10')
df_od_lat_lon=df_od_lat_lon.rename(columns={'INTPTLAT10': 'lat_h','INTPTLON10': 'lon_h'})
df_od_lat_lon=df_od_lat_lon.drop('GEOID10',1)

df_od_lat_lon.head()
print len(df_od_lat_lon)

# Because geo dataset only is for county 36061 a lot of elements in the join get NaN which we drop here
df_od_36061_lat_lon=df_od_lat_lon.dropna()
df_od_36061_lat_lon.head()
print len(df_od_36061_lat_lon)

print 'Our joining implies a filter because only geodata for county 36061 were taken into account'
print 'Ended joining OD and Geo data'
'''
################################################################################################################
#############################              A. Analysis bits							############################
################################################################################################################
'''
#####################
#1. Investigate sensitivities to number of commuters as link
#####################

#Investigate sensitivy of number of link properties to filtering on total number of jobs
#dict[number_of_minimum_jobs]=(unique home locations, unique work locations, total number of jobs)
sens_to_nbr_jobs_dict={}
len_evaluator=0
for i in range(max(df_od['S000'])+1):
	df_od_filter=df_od.loc[df_od['S000'] > i]
	unique_h=len(df_od_filter['h_geocode'].unique())
	unique_w=len(df_od_filter['w_geocode'].unique())
	unique_hw_combi=len(df_od_filter.groupby(['w_geocode','h_geocode']).size())
	total_jobs=sum(df_od_filter['S000'])
	sens_to_nbr_jobs_dict[i]=[unique_h,unique_w,unique_hw_combi,total_jobs]

sens_to_nbr_jobs_df = pd.DataFrame(sens_to_nbr_jobs_dict)
sens_to_nbr_jobs_df = sens_to_nbr_jobs_df.transpose()
sens_to_nbr_jobs_df.columns = ['unique_h', 'unique_w','unique_hw_combi','total_jobs'] 
#Index is 'filter_value_for_min_nmb_jobs',

#sens_to_nbr_jobs_df.head(10)

#Get log values to facilitate visualising
sens_to_nbr_jobs_df['log_unique_h']=np.log(sens_to_nbr_jobs_df['unique_h'])
sens_to_nbr_jobs_df['log_unique_w']=np.log(sens_to_nbr_jobs_df['unique_w'])
sens_to_nbr_jobs_df['log_unique_hw_combi']=np.log(sens_to_nbr_jobs_df['unique_hw_combi'])
sens_to_nbr_jobs_df['log_total_jobs']=np.log(sens_to_nbr_jobs_df['total_jobs'])

###############
#1.1 Figure Sensitivity to number of commuters
###############

#Create inset to show first 10 amounts.
fig, ax1=plt.subplots()
# These are in unitless percentages of the figure size. (0,0 is bottom left)
left, bottom, width, height = [0.25, 0.65, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])

ax1.plot(sens_to_nbr_jobs_df[['log_unique_h','log_unique_w','log_unique_hw_combi','log_total_jobs']])
ax1.set_xlim(0,300)
ax1.set_title('Sensitivity of commuting flows to minimun number of commuters (x)',fontsize=11)
ax1.set_ylabel('log(number)' ,fontsize=10)
ax1.set_xlabel('x for which the number of people commuting from home to work > x',fontsize=9)
ax1.legend(['unique home locations','unique work locations','unique home-work \n combinations','total number \n of commuters'],fontsize=8)

ax2.plot(sens_to_nbr_jobs_df[['log_unique_h','log_unique_w','log_unique_hw_combi','log_total_jobs']])
ax2.set_xlim(0,10)
ax2.set_ylim(6,16)

#plt.show()
plt.savefig('sens_to_nbr_jobs_log_unique_h_log_unique_w_log_unique_hw_combi_log_total_jobs_with_inset.png')
plt.cla(), plt.clf(); plt.close()

print 'end of the script'
'''

################################################################################################################
#############################              B. Visualisation bits							####################
################################################################################################################

#####################
#1. Plot coordinates and flows
#####################

#####################
#1.1 Plot coordinates
#####################
'''
plt.scatter(df_geo_small['INTPTLON10'],df_geo_small['INTPTLAT10'],s=2,alpha=0.5)
plt.show()
plt.cla(), plt.clf(); plt.close()
'''
#####################
#1.2 Plot flows
#####################

'''
# To start, we take a subset of the flows only. 
i = 10
df_od_36061_lat_lon_filter=df_od_36061_lat_lon.loc[df_od_36061_lat_lon['S000'] > i]

# Create lines to be drawn
lines=[]
#for index, row in df.iterrows(): #Itertuples is faster
for row in df_od_36061_lat_lon_filter.itertuples():
	line=[(row.lon_h,row.lat_h),(row.lon_w,row.lat_w)]
	#print line
	lines.append(line)

#Setup input for line collection
lines_array=np.array(lines)
weight=np.array(df_od_36061_lat_lon_filter['S000'])
weight_max=weight.max()
weight_min=weight.min()
#weight_lin_min=weight/weight_min #is an int

#Setup linecollection
#import matplotlib.colors as clr
lc = LineCollection(lines_array, cmap='RdYlBu_r',norm=clr.LogNorm(weight_min,weight_max))
#matplotlib.colors.LogNorm(vmin=None, vmax=None, clip=False)
#matplotlib.colors.NoNorm(vmin=None, vmax=None, clip=False)
#matplotlib.colors.Normalize(vmin=None, vmax=None, clip=False)
#matplotlib.colors.PowerNorm(gamma, vmin=None, vmax=None, clip=False)
#matplotlib.colors.SymLogNorm(linthresh, linscale=1.0, vmin=None, vmax=None, clip=False)

lc.set_array(weight)
lc.set_linewidth(1)
#lc.set_linewidth(weight_lin_min)
lc.set_alpha(0.4)

#Plot
fig, ax = plt.subplots(figsize=(14,12))
ax.scatter(df_geo_small['INTPTLON10'],df_geo_small['INTPTLAT10'],s=1,alpha=0.8, c='grey')
ax.add_collection(lc)
#ax.set_xlim(-74.03,-74.9)
#ax.set_ylim(40.65,40.9) #werkt niet
ax.autoscale_view()
ax.margins(0.1)
ax.set_title('Commuting flows at census block levels for New York city blocks')
ad_text= 'filtered on minimal ' + str(i) + ' commuters'
ax.annotate(ad_text, xy=(0.05, 0.95), xycoords='axes fraction')

#Setup colorbar, needs to have its own axes, so we make sure that axes is where we want it
left, bottom, width, height = [0.82, 0.13, 0.015, 0.3]
ax2 = fig.add_axes([left, bottom, width, height])
axcb=fig.colorbar(lc,cax=ax2)
axcb.set_label('Amount of commuters',rotation=270, va='bottom')

#Show or flush
#plt.tight_layout()
#plt.show()
plt.savefig('commuter_flows_NYC_censusblocks_min10.png')
plt.cla(), plt.clf(); plt.close()
'''




