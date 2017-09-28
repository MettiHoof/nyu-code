##############################################################################################

#Script to Read in the NHGIS data. 
#Created by Maarten on 17/09/2017

##############################################################################################

############################
#0. Setup environment
############################
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib import cm
import marble as mb


############################
#1. Read in data
############################

#####################
#1.1 Define inputfiles paths
#####################
# Define residential segregation files
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/'

# Parameter to define which classes we are going to work with. 
parameter='traveltime' #race, traveltime

if parameter=='income':
    print 'We will be working with ' + str(parameter)
    filename ='income_blockgroup_ny_2011_2015/nhgis0005_ds215_20155_2015_blck_grp.csv'
elif parameter=='race':
    print 'We will be working with ' + str(parameter)
    filename = 'race_blockgroup_ny_2011_2015/nhgis0004_ds215_20155_2015_blck_grp.csv'
if parameter=='traveltime':
    print 'We will be working with ' + str(parameter)
    filename= 'traveltime_blockgroup_ny_2011_2015/nhgis0006_ds215_20155_2015_blck_grp.csv'

inputfile= foldername+filename

# Define geo files
foldername_geo='/Users/maarten/Desktop/nyu-data/NHGIS/shapefile_ny_blockgroup_2015/'
inputname_geo= 'shapefile_blockgroup_NY_2015.csv'
inputfile_geo=foldername_geo + inputname_geo


#####################
#1.2 Read in segregation files
#####################

df_ny_full = pd.read_csv(inputfile, sep=',', lineterminator='\n')
print df_ny_full.head(3)

'''
Context Fields 
        GISJOIN:     GIS Join Match Code
        YEAR:        Data File Year
        REGIONA:     Region Code
        DIVISIONA:   Division Code
        STATE:       State Name
        STATEA:      State Code
        COUNTY:      County Name
        COUNTYA:     County Code
        COUSUBA:     County Subdivision Code
        PLACEA:      Place Code
        TRACTA:      Census Tract Code
        BLKGRPA:     Block Group Code
        CONCITA:     Consolidated City Code
        AIANHHA:     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
        RES_ONLYA:   American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only) Code
        TRUSTA:      American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land Code
        AITSCEA:     Tribal Subdivision/Remainder Code
        ANRCA:       Alaska Native Regional Corporation Code
        CBSAA:       Metropolitan Statistical Area/Micropolitan Statistical Area Code
        CSAA:        Combined Statistical Area Code
        METDIVA:     Metropolitan Division Code
        NECTAA:      New England City and Town Area Code
        CNECTAA:     Combined New England City and Town Area Code
        NECTADIVA:   New England City and Town Area Division Code
        UAA:         Urban Area Code
        CDCURRA:     Congressional District (2013-2017, 113th-114th Congress) Code
        SLDUA:       State Legislative District (Upper Chamber) Code
        SLDLA:       State Legislative District (Lower Chamber) Code
        ZCTA5A:      5-Digit ZIP Code Tabulation Area Code
        SUBMCDA:     Subminor Civil Division Code
        SDELMA:      School District (Elementary)/Remainder Code
        SDSECA:      School District (Secondary)/Remainder Code
        SDUNIA:      School District (Unified)/Remainder Code
        PUMA5A:      Public Use Microdata Sample Area (PUMA) Code
        BTTRA:       Tribal Census Tract Code
        BTBGA:       Tribal Block Group 
Income Estimates 
        NAME_E:      Area Name
        ADNJE001:    Total
        ADNJE002:    Less than $10,000
        ADNJE003:    $10,000 to $14,999
        ADNJE004:    $15,000 to $19,999
        ADNJE005:    $20,000 to $24,999
        ADNJE006:    $25,000 to $29,999
        ADNJE007:    $30,000 to $34,999
        ADNJE008:    $35,000 to $39,999
        ADNJE009:    $40,000 to $44,999
        ADNJE010:    $45,000 to $49,999
        ADNJE011:    $50,000 to $59,999
        ADNJE012:    $60,000 to $74,999
        ADNJE013:    $75,000 to $99,999
        ADNJE014:    $100,000 to $124,999
        ADNJE015:    $125,000 to $149,999
        ADNJE016:    $150,000 to $199,999
        ADNJE017:    $200,000 or more
Income margins of error
        ADNJM001:    Total
        ADNJM002:    Less than $10,000
        ADNJM003:    $10,000 to $14,999
        ADNJM004:    $15,000 to $19,999
        ADNJM005:    $20,000 to $24,999
        ADNJM006:    $25,000 to $29,999
        ADNJM007:    $30,000 to $34,999
        ADNJM008:    $35,000 to $39,999
        ADNJM009:    $40,000 to $44,999
        ADNJM010:    $45,000 to $49,999
        ADNJM011:    $50,000 to $59,999
        ADNJM012:    $60,000 to $74,999
        ADNJM013:    $75,000 to $99,999
        ADNJM014:    $100,000 to $124,999
        ADNJM015:    $125,000 to $149,999
        ADNJM016:    $150,000 to $199,999
        ADNJM017:    $200,000 or more
Race Estimates
		ADKXE001:    Total
        ADKXE002:    White alone
        ADKXE003:    Black or African American alone
        ADKXE004:    American Indian and Alaska Native alone
        ADKXE005:    Asian alone
        ADKXE006:    Native Hawaiian and Other Pacific Islander alone
        ADKXE007:    Some other race alone
        ADKXE008:    Two or more races
        ADKXE009:    Two or more races: Two races including Some other race
        ADKXE010:    Two or more races: Two races excluding Some other race, and three or more races
Race Margin of errors
        ADKXM001:    Total
        ADKXM002:    White alone
        ADKXM003:    Black or African American alone
        ADKXM004:    American Indian and Alaska Native alone
        ADKXM005:    Asian alone
        ADKXM006:    Native Hawaiian and Other Pacific Islander alone
        ADKXM007:    Some other race alone
        ADKXM008:    Two or more races
        ADKXM009:    Two or more races: Two races including Some other race
        ADKXM010:    Two or more races: Two races excluding Some other race, and three or more races
Travel time Estimates
        ADLOE001:    Total
        ADLOE002:    Less than 5 minutes
        ADLOE003:    5 to 9 minutes
        ADLOE004:    10 to 14 minutes
        ADLOE005:    15 to 19 minutes
        ADLOE006:    20 to 24 minutes
        ADLOE007:    25 to 29 minutes
        ADLOE008:    30 to 34 minutes
        ADLOE009:    35 to 39 minutes
        ADLOE010:    40 to 44 minutes
        ADLOE011:    45 to 59 minutes
        ADLOE012:    60 to 89 minutes
        ADLOE013:    90 or more minutes
Travel time Margins of errors
        ADLOM001:    Total
        ADLOM002:    Less than 5 minutes
        ADLOM003:    5 to 9 minutes
        ADLOM004:    10 to 14 minutes
        ADLOM005:    15 to 19 minutes
        ADLOM006:    20 to 24 minutes
        ADLOM007:    25 to 29 minutes
        ADLOM008:    30 to 34 minutes
        ADLOM009:    35 to 39 minutes
        ADLOM010:    40 to 44 minutes
        ADLOM011:    45 to 59 minutes
        ADLOM012:    60 to 89 minutes
        ADLOM013:    90 or more minutes
'''


#####################
#1.2 Simplify data
#####################

if parameter=='income':
    print 'Simplifying ' + str(parameter)

    df_ny=df_ny_full[
    [
    'GISJOIN',
    'ADNJE001', #Total
    'ADNJE002',
    'ADNJE003',
    'ADNJE004',
    'ADNJE005',
    'ADNJE006',
    'ADNJE007',
    'ADNJE008',
    'ADNJE009',
    'ADNJE010',
    'ADNJE011',
    'ADNJE012',
    'ADNJE013',
    'ADNJE014',
    'ADNJE015',
    'ADNJE016',
    'ADNJE017',
    ]]

    '''
    for index,row in df_income_ny.iterrows():
	   if row['ADNJE001'] == row['ADNJE002']+row['ADNJE003']+row['ADNJE004']+row['ADNJE005']+row['ADNJE006']+row['ADNJE007']+row['ADNJE008']+row['ADNJE009']+row['ADNJE010']+row['ADNJE011']+row['ADNJE012']+row['ADNJE013']+row['ADNJE014']+row['ADNJE015']+row['ADNJE016']+row['ADNJE017']:
		  print 'adds up to 100 percent'
	   else:
		  print 'houston we have a problem'
    '''

elif parameter=='race':
    print 'Simplifying ' + str(parameter)

    df_ny=df_ny_full[
    [
    'GISJOIN',
    'ADKXE001',#Total
    'ADKXE002',
    'ADKXE003',
    'ADKXE004',
    'ADKXE005',
    'ADKXE006',
    'ADKXE007',
    'ADKXE008',
    ]]
    # remark that we only work with the single races and one category for two or more races here as they percentages should sum up to 1 for our analysis
    '''
    for index,row in df_race_ny.iterrows():
    	if row['ADKXE001'] == row['ADKXE002']+row['ADKXE003']+row['ADKXE004']+row['ADKXE005']+row['ADKXE006']+row['ADKXE007']+row['ADKXE008']:
    		print 'adds up to 100 percent'
    	else:
    		print 'houston we have a problem'
    '''

elif parameter=='traveltime':
    print 'Simplifying ' + str(parameter)

    df_ny=df_ny_full[
    [
    'GISJOIN',
    'ADLOE001',#Total
    'ADLOE002',
    'ADLOE003',
    'ADLOE004',
    'ADLOE005',
    'ADLOE006',
    'ADLOE007',
    'ADLOE008',
    'ADLOE009',
    'ADLOE010',
    'ADLOE011',
    'ADLOE012',
    'ADLOE013',
    ]]

    '''
    for index,row in df_traveltime_ny.iterrows():
    	if row['ADLOE001'] == row['ADLOE002']+row['ADLOE003']+row['ADLOE004']+row['ADLOE005']+row['ADLOE006']+row['ADLOE007']+row['ADLOE008']+row['ADLOE009']+row['ADLOE010']+row['ADLOE011']+row['ADLOE012']+row['ADLOE013']:
    		print 'adds up to 100 percent'
    	else:
    		print 'houston we have a problem'
    '''



#print df_ny.head(10)

#####################
#1.3 Read in geo-data
#####################

print 'Reading in geo data'

df_geo = pd.read_csv(inputfile_geo,
    sep=',', 
    lineterminator='\n', 
    header=0,
    names = ['STATEFP','COUNTYFP','TRACTCE','BLKGRPCE','GEOID','NAMELSAD','MTFCC','FUNCSTAT','ALAND','AWATER','INTPTLAT','INTPTLON','GISJOIN','Shape_Leng','Shape_Area']
    )

print df_geo.head(3)
df_geo_small=df_geo[['GISJOIN','INTPTLAT','INTPTLON']]
print df_geo_small.head(3)
print 'Ended reading in geo data'


############################
#2. Read in data in marble
############################

#####################
#2.1 Prepare data for transformation to marble dict of dicts
#####################

# Marble treats the distribution of classes as a dict of dicts with
# dict[areal_unit][category] = number 
# e.g. city_dict = {"A":{0: 10, 1:0, 2:23},"B":{0: 0, 1:10, 2:8}}


# test case to get pandas dataframe to city_dict
#inp = [{'name':'A', '0':10, '1':0 , '2':23}, {'name':'B','0':0,'1':10, '2':8}]
#df = pd.DataFrame(inp)
#indexed_df = df.set_index(['name'])
#a= indexed_df.to_dict(orient='index') 
# a equals city_dict. nice


# Remove total field column 
#To delete the column without having to reassign df you can do:
#df.drop('column_name', axis=1, inplace=True)

# Btw, we get a copy so we don't mess with the original dataframe. 
df_ny_copy = df_ny.copy()

print 'preparing data for use in marble'
if parameter=='income':
    df_ny_copy.drop('ADNJE001', axis=1, inplace=True)
elif parameter=='race':
    df_ny_copy.drop('ADKXE001', axis=1, inplace=True)
elif parameter=='traveltime':
    df_ny_copy.drop('ADLOE001', axis=1, inplace=True)

#Set areal units as index
df_ny_indexed=df_ny_copy.set_index(['GISJOIN'])
#print df_ny_indexed.head(3)

#Transform to dict of dicts
dict_ny=df_ny_indexed.to_dict(orient='index')
#print dict_ny.items()[0]


############################
#3.  Calculate representation values for data. 
############################
print 'Starting caluclation of representation values'
r_dict= mb.representation(dict_ny)

# mb.representation its outcome is dict of dict with 
# {areal_id: {class_id: (representation_values, variance of the null model)}}

#####################
#3.1 Convert r_dicts to pandas dataframe 
#####################

def convert_r_dict_to_df(r_dict):
    r_df = pd.DataFrame([(area_id, class_id, tuple_of_r_outcomes) 
                        for area_id, dict_of_classes_and_rvalues in r_dict.items()
                        for class_id, tuple_of_r_outcomes in dict_of_classes_and_rvalues.items()
                        ])
    r_df.columns = ['area_id','class_id','tuple']
    r_df[['r_value', 'r_variance_null_model']] = r_df['tuple'].apply(pd.Series)
    r_df = r_df.drop('tuple', 1)

    return r_df

r_df=convert_r_dict_to_df(r_dict)


#####################
#3.2 Add information on statistically significant over- or under representation
#####################
# Remember that the expected values for r given the null model are 1, 
# implicating that 1 +/- 2.57*stdv of null models is the confidence interval
# for 99%.  The stdv of the null models equals the square root of its variance 

avg_exp_value_for_null_model = 1 #for gaussian distribution of nullmodel
confidence_interval_factor = 2.57 #for 99% interval of gaussidan distribution


###############
#3.2.1 Calculate z-score for value
###############
print 'starting calculation of z-scores for representation'
r_df['z_score']=(r_df['r_value'] - avg_exp_value_for_null_model) / pow(r_df['r_variance_null_model'],0.5)

###############
#3.2.2 Evaluate values at 99% interval
###############E
print 'starting evaluation of representation values for the 99 procent interval'
def r_value_to_signif_cat(row,confidence_interval_factor,avg_exp_value_for_null_model):
    value=row['r_value']
    stdv=pow(row['r_variance_null_model'],0.5) #stv, or variance, is specific for each class class combination
    boundary=stdv*confidence_interval_factor
    if value-boundary>=avg_exp_value_for_null_model:
        out='or' #significantly over-represented
    elif value+boundary<=avg_exp_value_for_null_model:
        out='ur' #signiifcantly under-represented
    else:
        out='ns' #non-significant
    return out

#axis=1 to pass row after row to the function, args requires a tuple if you have only one element, you need to add the comma at the end
r_df['signif_cat_99'] = r_df.apply(r_value_to_signif_cat,args=(confidence_interval_factor,avg_exp_value_for_null_model),axis=1)

###############
#3.2.3 Show some plots of distribution of z-scores
###############E
'''
print'showing some plots on the distribution of z_scores and 99 procent classes'
r_df['signif_cat_99'].value_counts().plot(kind='bar')
plt.show()

r_df.hist(column='z_score', bins=50)
plt.show()
'''
#####################
#3.3 Investigate spatial pattern of representation
#####################
print 'starting exploration of spatial patterns of representation'
#Join GEO-data information with representativity information.

# Unique area ids in r_income_signif_pandas_geo is 15463
# Unique GISJOIN codes in df_geo_small is 15246
# So we are losing data for 217 blockgroup resulting in 
# 217 * number of classes of NaN values for lat and lon 
# to see how much nans or nulls you have per columnr_income_signif_pandas_geo.isnull().sum()
print 'merging geo information with respresentation values'
r_df_geo=pd.merge(r_df,df_geo_small, how='left', left_on='area_id', right_on ='GISJOIN').rename(columns={'INTPTLAT': 'lat','INTPTLON': 'lon'})


#############
#3.3.1 Scatter for z-scores (continous)
#############
'''
print 'starting the creation of maps for z-scores of representation values'
# Get list of unique classes
class_id_list= r_df_geo.class_id.unique()

for class_id_name in class_id_list:

    df_one_class=r_df_geo.loc[r_df_geo['class_id'] == class_id_name]

    fig, ax1=plt.subplots(figsize=(14,12))
    sc=ax1.scatter(df_one_class['lon'],df_one_class['lat'], c=df_one_class['z_score'],cmap=cm.jet,vmin=-10,vmax=10,s=2,alpha=0.5)
    title_name='z_scores of representativity values for class %s in %s' %(class_id_name, parameter)
    ax1.set_title(title_name,fontsize=11) 

    ax1.set_xlim(-74.3,-73.5)
    ax1.set_ylim(40.49,41.05)
    plt.colorbar(sc)
    #plt.show()
    fig_name = 'representation_%s_NY_z_score_%s.png' %(parameter,class_id_name)
    plt.savefig(fig_name)
    plt.clf()
    plt.close()

'''
#############
#3.3.2 Scatter for significant test (categorical)
#############
'''
print 'starting the creation of maps for 99 procent classes of representation values'
# Get list of unique classes
class_id_list= r_df_geo.class_id.unique()

for class_id_name in class_id_list:

    df_one_class=r_df_geo.loc[r_df_geo['class_id'] == class_id_name]

    colors = {'or':'red', 'ur':'blue', 'ns':'grey'}

    fig, ax1=plt.subplots(figsize=(14,12))
    sc=ax1.scatter(df_one_class['lon'],df_one_class['lat'], c=df_one_class['signif_cat_99'].apply(lambda x: colors[x]),s=2,alpha=0.5)
    title_name='Significance of representativity values for class %s in %s' %(class_id_name,parameter)
    ax1.set_title(title_name,fontsize=11) 

    ax1.set_xlim(-74.3,-73.5)
    ax1.set_ylim(40.49,41.05)
    #plt.show()
    fig_name = 'representation_%s_NY_signif_cat_%s.png' %(parameter,class_id_name)
    plt.savefig(fig_name)
    plt.clf()
    plt.close()
'''
############################
#4.0  Calculate exposure values ourselves

# In marble it takes too much time; probably because of the calculation of the variance.
# Remakr that this means we can not add significancy scores to these calculations.  
############################
print 'Starting calculation of exposure values based on Maartens implementation'

def calc_exposure(r_df,n_df, n_total_df, r_areal_unit_name,n_areal_unit_name, alpha,beta):
    print alpha, beta

    #get total number of users in class alpha for all locations 
    total_alpha=n_total_df[alpha]

    #get n_alpha for all locations 
    n_alpha=n_df[[n_areal_unit_name,alpha]] #'GISJOIN'  

    #get r_beta for all locations
    r_beta_all=r_df.loc[r_df['class_id'] == beta]
    r_beta= r_beta_all[[r_areal_unit_name,'class_id','r_value']] #'GISJOIN'
   
    # join n_alpha and r_beta based on area ids.
    alpha_beta_merge=pd.merge(n_alpha,r_beta, how='left', left_on=n_areal_unit_name, right_on =r_areal_unit_name).rename(columns={alpha:'n_alpha','class_id': 'class_id_beta','r_value': 'r_value_beta'})

    alpha_beta_merge['exposure_tussen']=alpha_beta_merge['n_alpha']*alpha_beta_merge['r_value_beta']
    sum_alpha_beta=alpha_beta_merge['exposure_tussen'].sum()

    exposure=sum_alpha_beta/total_alpha

    return exposure


#df_ny gives the amount of people per areal unit, per class. 
#df_ny sum gives the amount of people per class for the entire area
df_ny_sum = df_ny.sum()
#r_df gives the representation values per calls and per areal unit. 

# Fill dict with exposure values
class_id_list= r_df.class_id.unique()

exp_dict={}
for class_id in class_id_list:
    exp_dict[class_id]={}
for class_id in class_id_list:
        for class_id2 in class_id_list:
            exp_dict[class_id][class_id2]=calc_exposure(r_df,df_ny,df_ny_sum,'area_id','GISJOIN',class_id,class_id2)


def convert_exp_dict_to_df(exp_dict):
    exp_df=pd.DataFrame([(class_id1, class_id2, tuple_of_exp_outcomes) 
                            for class_id1, dict_of_classes_and_exp_values in exp_dict.items()
                                for class_id2, tuple_of_exp_outcomes in dict_of_classes_and_exp_values.items()
                                        ])
    exp_df.columns = ['class_id1','class_id2','exp_value']
    # Voor de eigen implementatie hebben we geen tuple. 
    #exp_df.columns = ['class_id1','class_id2','tuple']
    #exp_df[['exp_value', 'exp_variance_null_model']] = exp_df['tuple'].apply(pd.Series)           
    #exp_df = exp_df.drop('tuple', 1)
    exp_df_copy=exp_df.copy()
    
    return exp_df_copy

exp_df=convert_exp_dict_to_df(exp_dict)


############################
#4.  Calculate exposure values for data based on marble. 
############################

#print 'Starting calculation of exposure values'
#exp_dict= mb.exposure(dict_ny)

# mb.exposure its outcome is dict of dict with 
# {class_id: {class_id: (exposure value, variance of the null model)}}


############################
#4.1 Add information on significancy 

#####################   OPGEPAST !!!!!!  ##################
# Grote vraag is of de exposure values ook de gaussian distributie vormen en of dus hiervoor ook geldt dat
#2,57 * stdv is het 99% interval. Het zou wel eens kunnen zijn dat dit niet waar is.

############################

###############
#4.1.1 Set up significancy parameters 
###############
'''
# Set up significacy parameters. 
avg_exp_value_for_null_model = 1 # average exposure value for nullmodel = 1 (see paper Louf et Barthelemy)
confidence_interval_factor = 2.57 #for 99% interval of gaussidan distribution
'''
###############
#4.1.2 Change dataformat
###############
'''
# Put in pandas format to make it more workable. 
city = {"A":{0: 10, 1:0, 2:23},"B":{0: 0, 1:10, 2:8}}
test = mb.exposure(city)

def convert_exp_dict_to_df(exp_dict):
    exp_df=pd.DataFrame([(class_id1, class_id2, tuple_of_exp_outcomes) 
                            for class_id1, dict_of_classes_and_exp_values in exp_dict.items()
                                for class_id2, tuple_of_exp_outcomes in dict_of_classes_and_exp_values.items()
                                        ])
    exp_df.columns = ['class_id1','class_id2','tuple']
    exp_df[['exp_value', 'exp_variance_null_model']] = exp_df['tuple'].apply(pd.Series)           
    exp_df = exp_df.drop('tuple', 1)
    exp_df_copy=exp_df.copy()
    return exp_df_copy

exp_df=convert_exp_dict_to_df(exp_dict)
'''
###############
#4.1.3 Calculate z-score 
###############
'''
exp_df['z_score']=(exp_df['exp_value'] - avg_exp_value_for_null_model) / pow(exp_df['exp_variance_null_model'],0.5)
'''
###############
#4.1.3 Evaluate z_score at 99% interval
###############E
'''
def exp_value_to_signif_cat(row,confidence_interval_factor,avg_exp_value_for_null_model):
    value=row['exp_value']
    stdv=pow(row['exp_variance_null_model'],0.5) #stv, or variance, is specific for each class class combination
    boundary=stdv*confidence_interval_factor
    if value-boundary>=avg_exp_value_for_null_model:
        out='or'
    elif value+boundary<=avg_exp_value_for_null_model:
        out='ur'
    else:
        out='ns'
    return out

#axis=1 to pass row after row to the function, args requires a tuple if you have only one element, you need to add the comma at the end
exp_df['signif_cat_99'] = exp_df.apply(exp_value_to_signif_cat,args=(confidence_interval_factor,avg_exp_value_for_null_model),axis=1)

'''
############################
#4.2 Create Hinton diagrams for exposure values. 
############################

def hinton(df_matrix, ax=None):
    """Draw Hinton diagram for visualizing a weight matrix."""
    ax = ax if ax is not None else plt.gca()

    ax.patch.set_facecolor('lightgray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    max_value=df_matrix.values.max()

    for (x, y), w in np.ndenumerate(df_matrix):
        # for exposure, w is gonna range between 0 and max_value
        # we size the surface of the square with the biggest being one on one. 
        color = 'red' if w > 1 else 'blue'
        size = np.square(w/max_value)
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    nticks = df_matrix.shape[0]
    ax.xaxis.tick_top()
    ax.set_xticks(range(nticks))
    ax.set_xticklabels(list(df_matrix.columns), rotation=90)
    ax.set_yticks(range(nticks))
    ax.set_yticklabels(df_matrix.columns)
    ax.grid(False)

    ax.autoscale_view()
    ax.invert_yaxis()

#Put data in right format
exp_df_for_hinton = exp_df.pivot(index='class_id1', columns='class_id2', values='exp_value')
#Create, show or save hinton
hinton(exp_df_for_hinton)
title_name= 'Hinton diagram of exposure values for %s in NY state.png' %parameter
plt.title(title_name)

#plt.show()
fig_name = 'Hinton_%s_NY.png' %parameter
plt.savefig(fig_name)

plt.close()



###############################################################################################
###################################      Developing        ####################################
###############################################################################################



"""

r_test={'G36006300241022': 
  {'ADNJE002': (0.0, 0.04508635422989736),
  'ADNJE003': (0.27074082779052672, 0.067682569357755809),
  'ADNJE004': (1.5561543464954604, 0.070731532069106984),
  'ADNJE005': (0.51209694666194505, 0.073153855860069311),
  'ADNJE006': (1.9187321424781343, 0.079944057183172351),
  'ADNJE007': (1.4433027906558002, 0.080180363740816385),
  'ADNJE008': (0.0, 0.087008348792340345),
  'ADNJE009': (0.95964764714385331, 0.087237295557297131),
  'ADNJE010': (1.1865522491411293, 0.098875500916607156),
  'ADNJE011': (1.3061543459261695, 0.050234747964306964),
  'ADNJE012': (1.9675117019710866, 0.037835289058146641),
  'ADNJE013': (1.6648849249493951, 0.029728929409080829),
  'ADNJE014': (1.7796737704962224, 0.040445554984275232),
  'ADNJE015': (0.44019335309154112, 0.062882314203441009),
  'ADNJE016': (0.0, 0.054714130902507672),
  'ADNJE017': (0.0, 0.046904441442265736)}
  }

"""






'''
city = {"A":{0: 10, 1:0, 2:23},"B":{0: 0, 1:10, 2:8}}

co = mb.concentration(city)
print co['A'][0]

1.0

pr = mb.proportion(city)
print pr['A'][0]

0.303

rep = mb.representation(city)
print rep['A'][0]

(1.55, 0.054)




#########
#2.1.1 Create helperfunction to get any x first values from a list. 
#n_items = take(n, d.iteritems())
#########


def take(n, iterable):
        from itertools import islice
        "Return any first n items of the iterable as a list"
        return list(islice(iterable, n))

#n_items = take(n, dict_name.iteritems())

print take(3,income_ny_dict)


def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

print pretty(income_ny_dict)




# Prepare small helper function to get GEO-ID from geo_data_small in right shape to join

def add_G (row):
    row_out = 'G'  + str(row)
    return row_out


df_geo_small['GEOID10_with_G'] = df_geo_small['GEOID10'].apply(add_G)


'''

