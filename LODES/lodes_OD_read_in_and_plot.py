##############################################################################################

#Script to Read in the LODES data. 
#Created by Maarten on 06/09/2017

##############################################################################################

############################
#0. Setup environment
############################
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as clr
from matplotlib.collections import LineCollection

############################
#1. Read in Lodes OD files
############################

#####################
#1.1 Define inputfiles
#####################
foldername='/Users/maarten/Desktop/nyu-data/LEHD/OD/'

statename='ny'
typename='_od_main' 
#_od_main (both home and work within state)
#_od_aux (work in state, home outside state)
groupname='_JT00' 
#_JT000 (all jobs) 
#_JT001 (primary jobs)
#_JT002 (All private jobs)
#_JT003 (Private primary jobs)
#_JT004 (All federal jobs)
#_JT005 (Federal primary jobs) 
year='_2010'
extension='.csv'

filename=statename+typename+groupname+year+extension

inputfile=foldername+filename
#print inputfile

#####################
#1.2 Read in OD files
#####################

df_od = pd.read_csv(inputfile,
	sep=',', 
	lineterminator='\n', 
	)
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

print df_od.head(10)
df_od_small=df_od[['w_geocode','h_geocode','S000']]

print 'Ended reading in OD files'

############################
#2. Read in lat lon info for census blocks 

##!!!! Opgepast, we hebben de data hier enkel voor New York City county, 
##andere counties moeten apart worden gedownload:

###########################


#####################
#2.1 Define inputfiles
# The NY_36061_NY_blocks_lat_lon was made based on the 2010_NY_36061_NY_blocks_boundary_files shapefile, then in qgis. 
#####################

print 'Reading in geo data'

foldername_geo='/Users/maarten/Desktop/nyu-data/Geo_lookup_shp/'
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

############################
#3. Join Lodes OD with Lat lon info
############################
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




