##############################################################################################
# Script to map the informations on z-scores

# Data based on preparation in nhgis_us_tract_data_creation_perstate_null_model.py 
# This means the null models were created per state individually, at census tract level 

# Script written by Maarten on 13/10/2017
##############################################################################################
############################
#0. Setup environment
############################
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib import cm
import copy


# Parameter to define which classes we are going to work with. 
parameter='race' #income, race, traveltime, transportationmeans


#####################
#1. Prepare work dataframes by reading in data from nhgis_us_tract_data_creation_perstate_null_model.py 
#####################f

print 'Start loading of df_n_z_score_all_states from pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_n_z_weighted_z_nullmodel_perstate.pkl' %(parameter,parameter)
picklename=foldername+filename

df_n_z=pd.read_pickle(picklename)

# There are a lot of columns in df_n_z that you could use.  x are the z_scores, y are the population counts
# 		u'ADKXE002_z_score', u'ADKXE003_z_score', u'ADKXE004_z_score', u'ADKXE005_z_score',
#       u'ADKXE006_z_score', u'ADKXE007_z_score', u'ADKXE008_z_score', u'STATEA', u'ADKXE001',
#       u'ADKXE002_pop', u'ADKXE003_pop', u'ADKXE004_pop', u'ADKXE005_pop',
#       u'ADKXE006_pop', u'ADKXE007_pop', u'ADKXE008_pop',
#       u'ADKXE008_populated_z_score', u'ADKXE008_populated_z_score_abs',
#       u'ADKXE003_populated_z_score', u'ADKXE003_populated_z_score_abs',
#       u'ADKXE002_populated_z_score', u'ADKXE002_populated_z_score_abs',
#       u'ADKXE005_populated_z_score', u'ADKXE005_populated_z_score_abs',
#       u'ADKXE004_populated_z_score', u'ADKXE004_populated_z_score_abs',
#       u'ADKXE007_populated_z_score', u'ADKXE007_populated_z_score_abs',
#       u'ADKXE006_populated_z_score', u'ADKXE006_populated_z_score_abs',
#       u'abs_sum', u'total_pop', u'weighted_abs_z_score',
#       u'ADKXE008_pop_percentage', u'ADKXE003_pop_percentage',
#       u'ADKXE002_pop_percentage', u'ADKXE005_pop_percentage',
#       u'ADKXE004_pop_percentage', u'ADKXE007_pop_percentage',
#       u'ADKXE006_pop_percentage'],
print 'Ended loading of df_n_z_score_all_states from pickle'

#####################
#1.1 Prepare population data from df_n_z 
#####################
print 'Start preparation of population data'
n_cols = [col for col in df_n_z.columns if '_pop' in col[-4:]] 
n_perc_cols=[col for col in df_n_z.columns if '_pop_percentage' in col]

selection_n=copy.copy(n_cols)
selection_n.extend(n_perc_cols)
selection_n.append('total_pop')

df_n=df_n_z[selection_n].copy()

#####################
#1.2 Prepare z-score data from df_n_z 
#####################
print 'Start preparation of z-score data'

z_cols = [col for col in df_n_z.columns if '_z_score' in col]
z_pop_cols = [col for col in df_n_z.columns if '_populated_z_score' in col[-17:]]
z_pop_abs_cols = [col for col in df_n_z.columns if '_populated_z_score_abs' in col]

selection_z=copy.copy(z_cols)
selection_z.extend(z_pop_cols)
selection_z.extend(z_pop_abs_cols)
selection_z.append('weighted_abs_z_score')

df_z=df_n_z[selection_z].copy()

#####################
#1.3 Prepare r-values data  
#####################
print 'Start preparation of r_value data'

# Get full results of representation analysis. 
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_r_nullmodel_perstate.pkl' %(parameter,parameter)
picklename=foldername+filename

r_df_all_states=pd.read_pickle(picklename)

# Pivot r_df to a df with index aread_id, columns class_id values and as values, the calculated r_values
df_r=r_df_all_states.pivot(index='area_id', columns='class_id', values='r_value').copy()

# If you don't specify values in pivot, he creates a hierarchical dataframe for all columns that are not in the pivot command
# You can thus access a pivoted table for all columns by typing r_df_all_states_pivot['columname']
# Options for values or r_df_all_states[columnname] are
# z_score
# r_values
# r_variance_null_model
# signif_cat_99


#####################
#1.4 Prepare r-values significant data  
#####################
print 'Start preparation of r_value significancy data'
df_r_sign=r_df_all_states.pivot(index='area_id', columns='class_id', values='signif_cat_99').copy()

print df_n.shape
print df_z.shape
print df_r.shape
print df_r_sign.shape


#####################
#2. Prepare geo_data
#####################

print 'Reading in geo data'
# Define geo files
foldername_geo='/Users/maarten/Desktop/nyu-data/NHGIS/shapefiles/shapefiles_us_in_csv_format/'
inputname_geo= 'shapefile_us_censustract_2015.csv'
inputfile_geo=foldername_geo + inputname_geo


inputfile_geo_trct='/Users/maarten/Desktop/nyu-data/NHGIS/shapefiles/shapefiles_us_in_csv_format/shapefile_us_censustract_2015.csv'
# STATEFP,COUNTYFP,TRACTCE,GEOID,NAME,NAMELSAD,MTFCC,FUNCSTAT,ALAND,AWATER,INTPTLAT,INTPTLON,GISJOIN,Shape_Leng,Shape_Area
# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
dtype_dict_trct={'STATEFP': object,'GEOID': object,'GISJOIN':object}
df_geo_trct = pd.read_csv(inputfile_geo_trct,sep=',',lineterminator='\n',dtype=dtype_dict_trct)
df_geo_trct_small=df_geo_trct[['STATEFP','GISJOIN','INTPTLAT','INTPTLON']]
df_geo_trct_small=df_geo_trct_small.set_index('GISJOIN')


#####################
#2. Join geodata 
#####################

#####################
#2.1 Define helperfunctions
#####################

def join_geo(inputfile,geofile):
	'''We expect inputfile and geofile to have the same index'''
	print 'Start join GEO for'
	df_geo=pd.merge(inputfile,geofile,how='left', left_index=True, right_index =True).rename(columns={'INTPTLAT': 'lat','INTPTLON': 'lon'})
	print 'There are ' + str(df_geo.isnull().sum()['lat']) + ' rows that were not succesfully joined and hence have no lat-lon coordinates'
	
	return df_geo

df_n_geo=join_geo(df_n,df_geo_trct_small)
df_z_geo=join_geo(df_z,df_geo_trct_small)
df_r_geo=join_geo(df_r,df_geo_trct_small)
df_r_sign_geo=join_geo(df_r_sign,df_geo_trct_small)


#####################
#2. Map simple scatterplot of entire USA 
# We will map the values (r-values, z-scores, populuations..) for each class that is in the dataframe  
#####################

#####################
#2.1 Define helperfunctions
#####################

for i in range(10):
    print i

def map_usa(df,parameter,value_name):

    print 'Starting simple scatterplot plotting for the entire USA'

    #Check whether we have a lat lon name in the columns. we are expecting this. 
    if ('lat' in df.columns and 'lon' in df.columns):
        cols_to_treat=list(df.columns)
        cols_to_treat.remove('lat')
        cols_to_treat.remove('lon')
        cols_to_treat.remove('STATEFP')
    else:
        print 'there are no columns with lat and/or lon names'

    for class_id in cols_to_treat:
        print class_id
        
        #Set up names
        title_name= 'Analysis of %s' %class_id
        label_colorbar=value_name
        figname='map_%s_%s_null_model_per_state.png'%(parameter,class_id)
        outputfolder='/Users/maarten/Desktop/nyu-code/residential_segregation/maps_%s_null_model_per_state/'%parameter
        outputname=outputfolder+figname
        #Set up figure 
        fig, ax1=plt.subplots(figsize=(18,12))
        sc=ax1.scatter(df['lon'],df['lat'], c=df[class_id],cmap=cm.hot_r,s=1,alpha=0.5)
        #Make up figure
        ax1.set_title(title_name,fontsize=11)
        ax1.margins(0,1)
        ax1.set_xlim(-130,-65)
        ax1.set_ylim(24,50)
        #Make up colorbar
        ax2=fig.add_axes([0.82, 0.13, 0.015, 0.3]) #left, bottom, width, height)
        axcb=fig.colorbar(sc,cax=ax2)
        axcb.set_label(label_colorbar,rotation=270,va='bottom')

        #show
        #plt.show

        #save
        plt.savefig(outputname)
        plt.cla()
        plt.clf()
        plt.close('all')

        print 'Finished a map'

    return 'tettn'

map_usa(df_n_geo,parameter,'population')
map_usa(df_z_geo,parameter,'z-score')


'''

print 'Starting mapping of ' + str(class_id)

# Set up names
title_name=' for in analysis of '

# Set up figure
fig, ax1=plt.subplots(figsize=(18,12))

# Plot scatter
sc=ax1.scatter(df['lon'],df['lat'], c=df[class_id],cmap=cm.hot_r, s=1, alpha=0.5)

# Make up figure
ax1.set_title(title_name,fontsize=11)
ax1.margins(0.1)
ax1.set_xlim(-130,-65) # To not show alaska, puerto rico and other weird territories
ax1.set_ylim(24,50)
print 'halfway'

ax2 = fig.add_axes([0.82, 0.13, 0.015, 0.3]) #left, bottom, width, height
axcb=fig.colorbar(sc,cax=ax2)
label=value_name
axcb.set_label(label,rotation=270, va='bottom')

print 'saving'
figname='map_test_%s_%s.png' %(class_id,parameter)
outfolder='/Users/maarten/Desktop/nyu-code/residential_segregation/test/'
plt.savefig(outputname)
plt.cla(),plt.clf,plt.close('all')
'''

'''
print 'Starting the creation of maps for z-scores of representation values'
# Get list of unique classes
class_id_list= r_df_geo.class_id.unique()

for class_id_name in class_id_list:

    df_one_class=r_df_geo.loc[r_df_geo['class_id'] == class_id_name]

    fig, ax1=plt.subplots(figsize=(18,12))
    sc=ax1.scatter(df_one_class['lon'],df_one_class['lat'], c=df_one_class['z_score'],cmap=cm.jet,vmin=-10,vmax=10,s=2,alpha=0.5)
    title_name='z_scores of representativity values for class %s in %s' %(class_id_name, parameter)
    ax1.set_title(title_name,fontsize=11) 

    #ax1.autoscale_view()
    ax1.margins(0.1) # Margins to the side of the figure
    # To not show alaska, puerto rico and other weird territories
    ax1.set_xlim(-130,-65)
    ax1.set_ylim(24,50)

    # Setup colorbar
    left, bottom, width, height = [0.82, 0.13, 0.015, 0.3]
    ax2 = fig.add_axes([left, bottom, width, height])
    axcb=fig.colorbar(sc,cax=ax2)
    label='z-scores'
    axcb.set_label(label,rotation=270, va='bottom')

    #plt.show()
    
    figname = 'figures_US_%s_censustracts_2015_r/map_z-score_r_%s_%s_us_tract_2015.png' %(parameter,parameter,class_id_name)
    outputname=outputfolder+figname
    plt.savefig(outputname)
    plt.clf()
    plt.close('all')

print 'Ended the creation of maps for z-scores of representation values'





df_n_r_z_geo=pd.merge(df_n_r_z,df_geo_trct_small, how='left', left_index=True, right_index =True).rename(columns={'INTPTLAT': 'lat','INTPTLON': 'lon'})


print 'We lost ' + str(df_n_r_z_geo.isnull().sum()['GEOID']) + ' rows by performing joins'
print 'There are ' + str(df_n_r_z_geo.isnull().sum()[r_cols[0]]) + ' rows that dont have an rvalue and thus neither z-scores etc' 
print 'There are ' + str(df_n_r_z_geo.isnull().sum()[n_cols[0]]) + ' rows that dont have an population counts and thus no trustworthy weighted z_scores etc'

#Filter out NaNs
df_n_r_z_geo_nona = df_n_r_z_geo.dropna()
#print df_n_r_z_geo.shape
#print df_n_r_z_geo_nona.shape
#print df_n_r_z_geo_nona.isnull().sum()
'''




'''

#####################
#6.1.3 Read in population data
#####################

print 'Start loading of df_n_z_score_all_states from pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_n_z_weighted_z_nullmodel_perstate.pkl' %(parameter,parameter)
picklename=foldername+filename

df_n_z=pd.read_pickle(picklename)

print 'Ended loading of df_n_z_score_all_states from pickle'

n_cols = [col for col in df_n_z.columns if '_y' in col] #_y are the populationcounts in the pythonscript before. Attributed by a merge there
n_perc_cols=[col for col in df_n_z.columns if '_pop_percentage' in col]

selection=copy.copy(n_cols)
selection.extend(n_perc_cols)
selection.append('total_pop')
print selection
df_n_z_selection=df_n_z[selection].copy()
print df_n_z_selection.head()


#####################
#6.1.2 Read in geo data
#####################
print 'Reading in geo data'
# Define geo files
foldername_geo='/Users/maarten/Desktop/nyu-data/NHGIS/shapefiles/shapefiles_us_in_csv_format/'
inputname_geo= 'shapefile_us_censustract_2015.csv'
inputfile_geo=foldername_geo + inputname_geo


inputfile_geo_trct='/Users/maarten/Desktop/nyu-data/NHGIS/shapefiles/shapefiles_us_in_csv_format/shapefile_us_censustract_2015.csv'
# STATEFP,COUNTYFP,TRACTCE,GEOID,NAME,NAMELSAD,MTFCC,FUNCSTAT,ALAND,AWATER,INTPTLAT,INTPTLON,GISJOIN,Shape_Leng,Shape_Area
# Make sure we read in the columns we need as strings, otherwise pandas might omit zeroes at the beginning of the number, messing up joins later on. 
dtype_dict_trct={'STATEFP': object,'GEOID': object,'GISJOIN':object}
df_geo_trct = pd.read_csv(inputfile_geo_trct,sep=',',lineterminator='\n',dtype=dtype_dict_trct)
df_geo_trct_small=df_geo_trct[['STATEFP','GEOID','GISJOIN','INTPTLAT','INTPTLON']]
df_geo_trct_small=df_geo_trct_small.set_index('GISJOIN')


#####################
#6.2 Join r_df_all_states and df_n_z_selection
#####################

print 'Join r_df_all_states and df_n_z_selection'

df_r_n_z=pd.merge(r_df_all_states,df_n_z_selection, how='left', left_index=True, right_index =True)

print df_r_n_z.isnull().sum()

'''
'''
print 'Join r_df_all_states and df_n_z_selection'
df_n_r_z_geo=pd.merge(df_n_r_z,df_geo_trct_small, how='left', left_index=True, right_index =True).rename(columns={'INTPTLAT': 'lat','INTPTLON': 'lon'})

#####################
#6.2.1 Investigate properties of data and filter out nans. 
#####################

print 'We lost ' + str(df_n_r_z_geo.isnull().sum()['GEOID']) + ' rows by performing joins'
print 'There are ' + str(df_n_r_z_geo.isnull().sum()[r_cols[0]]) + ' rows that dont have an rvalue and thus neither z-scores etc' 
print 'There are ' + str(df_n_r_z_geo.isnull().sum()[n_cols[0]]) + ' rows that dont have an population counts and thus no trustworthy weighted z_scores etc'

#Filter out NaNs
df_n_r_z_geo_nona = df_n_r_z_geo.dropna()
#print df_n_r_z_geo.shape
#print df_n_r_z_geo_nona.shape
#print df_n_r_z_geo_nona.isnull().sum()
'''

