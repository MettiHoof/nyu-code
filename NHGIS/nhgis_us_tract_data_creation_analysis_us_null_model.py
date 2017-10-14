##############################################################################################

# Performing residential segregation analysis on census data at tract level for the USA - nhgis. 

# For a null model that incorporates the entire usa. 

# Script written by Maarten on 12/10/2017

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
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'

# Parameter to define which classes we are going to work with. 
parameter='race' #income, race, traveltime, transportationmeans

print 'We will be working with ' + str(parameter)
filename ='%s_censustracts_us_2015/%s_censustracts_us_2015.csv' %(parameter,parameter)
inputfile= foldername+filename
print inputfile


#####################
#1.2 Read in census data
#####################

dtype_dict_trct={'STATEA': object,'TRACTA': object,'GISJOIN':object}
df_us_full = pd.read_csv(inputfile, sep=',', lineterminator='\n',dtype=dtype_dict_trct)

'''
Context Fields 
        GISJOIN:     GIS Join Match Code  - at different levels of aggregation depending on the file. 
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
Transportation means Estimates
        ADLME001:    Total
        ADLME002:    Car, truck, or van
        ADLME003:    Car, truck, or van: Drove alone
        ADLME004:    Car, truck, or van: Carpooled
        ADLME005:    Car, truck, or van: Carpooled: In 2-person carpool
        ADLME006:    Car, truck, or van: Carpooled: In 3-person carpool
        ADLME007:    Car, truck, or van: Carpooled: In 4-person carpool
        ADLME008:    Car, truck, or van: Carpooled: In 5- or 6-person carpool
        ADLME009:    Car, truck, or van: Carpooled: In 7-or-more-person carpool
        ADLME010:    Public transportation (excluding taxicab)
        ADLME011:    Public transportation (excluding taxicab): Bus or trolley bus
        ADLME012:    Public transportation (excluding taxicab): Streetcar or trolley car (carro publico in Puerto Rico)
        ADLME013:    Public transportation (excluding taxicab): Subway or elevated
        ADLME014:    Public transportation (excluding taxicab): Railroad
        ADLME015:    Public transportation (excluding taxicab): Ferryboat
        ADLME016:    Taxicab
        ADLME017:    Motorcycle
        ADLME018:    Bicycle
        ADLME019:    Walked
        ADLME020:    Other means
        ADLME021:    Worked at home
Transportation means margins of error
        ADLMM001:    Total
        ADLMM002:    Car, truck, or van
        ADLMM003:    	Car, truck, or van: Drove alone
        ADLMM004:    	Car, truck, or van: Carpooled
        ADLMM005:    		Car, truck, or van: Carpooled: In 2-person carpool
        ADLMM006:    		Car, truck, or van: Carpooled: In 3-person carpool
        ADLMM007:    		Car, truck, or van: Carpooled: In 4-person carpool
        ADLMM008:    		Car, truck, or van: Carpooled: In 5- or 6-person carpool
        ADLMM009:    		Car, truck, or van: Carpooled: In 7-or-more-person carpool
        ADLMM010:    Public transportation (excluding taxicab)
        ADLMM011:    	Public transportation (excluding taxicab): Bus or trolley bus
        ADLMM012:    	Public transportation (excluding taxicab): Streetcar or trolley car (carro publico in Puerto Rico)
        ADLMM013:    	Public transportation (excluding taxicab): Subway or elevated
        ADLMM014:    	Public transportation (excluding taxicab): Railroad
        ADLMM015:    	Public transportation (excluding taxicab): Ferryboat
        ADLMM016:    Taxicab
        ADLMM017:    Motorcycle
        ADLMM018:    Bicycle
        ADLMM019:    Walked
        ADLMM020:    Other means
        ADLMM021:    Worked at home
'''


#####################
#1.2 Simplify data
#####################

if parameter=='income':
    print 'Simplifying ' + str(parameter)

    df_us=df_us_full[
    [
    'GISJOIN',
    'STATEA',
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

    
    #for index,row in df_us.iterrows():
	#   if row['ADNJE001'] == row['ADNJE002']+row['ADNJE003']+row['ADNJE004']+row['ADNJE005']+row['ADNJE006']+row['ADNJE007']+row['ADNJE008']+row['ADNJE009']+row['ADNJE010']+row['ADNJE011']+row['ADNJE012']+row['ADNJE013']+row['ADNJE014']+row['ADNJE015']+row['ADNJE016']+row['ADNJE017']:
	#	  print 'adds up to 100 percent'
	#   else:
	#	  print 'houston we have a problem'
    

elif parameter=='race':
    print 'Simplifying ' + str(parameter)

    df_us=df_us_full[
    [
    'GISJOIN',
    'STATEA',
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
    
    #for index,row in df_us.iterrows():
    #	if row['ADKXE001'] == row['ADKXE002']+row['ADKXE003']+row['ADKXE004']+row['ADKXE005']+row['ADKXE006']+row['ADKXE007']+row['ADKXE008']:
    #		print 'adds up to 100 percent'
    #	else:
    #		print 'houston we have a problem'
    

elif parameter=='traveltime':
    print 'Simplifying ' + str(parameter)

    df_us=df_us_full[
    [
    'GISJOIN',
    'STATEA',
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

    
    #for index,row in df_us.iterrows():
    #	if row['ADLOE001'] == row['ADLOE002']+row['ADLOE003']+row['ADLOE004']+row['ADLOE005']+row['ADLOE006']+row['ADLOE007']+row['ADLOE008']+row['ADLOE009']+row['ADLOE010']+row['ADLOE011']+row['ADLOE012']+row['ADLOE013']:
    #		print 'adds up to 100 percent'
    #	else:
    #		print 'houston we have a problem'
    


elif parameter=='transportationmeans':
    print 'Simplifying ' + str(parameter)

    df_us=df_us_full[
    [
    'GISJOIN',
    'STATEA',
    'ADLME001', #Total
    'ADLME002',
    'ADLME010',
    'ADLME016',
    'ADLME017',
    'ADLME018',
    'ADLME019',
    'ADLME020',
    'ADLME021',
    ]]
    # remark that we only work with certain categories as the percentages should sum up to 1. We could unfold more categories though if we wished. 
    
    
    #for index,row in df_us.iterrows():	
    #	if row['ADLME001'] == row['ADLME002']+row['ADLME003']+row['ADLME004']+row['ADLME005']+row['ADLME006']+row['ADLME007']+row['ADLME008']+row['ADLME009']+row['ADLME010']+row['ADLME011']+row['ADLME012']+row['ADLME013']+row['ADLME014']+row['ADLME015']+row['ADLME016']+row['ADLME017']+row['ADLME018']+row['ADLME019']+row['ADLME020']+row['ADLME021']:
    #		print 'all rows together add up to 100 percent'
    #	elif row['ADLME001'] == row['ADLME002']+row['ADLME010']+row['ADLME016']+row['ADLME017']+row['ADLME018']+row['ADLME019']+row['ADLME020']+row['ADLME021']:
    #		print 'some speficic rows together add up to 100 percent'
    #	else:
    #		print 'houston we have a problem'
    
 

############################
#2. Read in data in marble
############################

#####################
#2.1 Prepare data for transformation to marble dict of dicts
#####################

# Marble treats the distribution of classes as a dict of dicts with
# dict[areal_unit][category] = number 
# e.g. city_dict = {"A":{0: 10, 1:0, 2:23},"B":{0: 0, 1:10, 2:8}}


# Btw, we get a copy so we don't mess with the original dataframe. 
df_us_copy = df_us.copy()

print 'preparing data for use in marble'
if parameter=='income':
    df_us_copy.drop('ADNJE001', axis=1, inplace=True)
elif parameter=='race':
    df_us_copy.drop('ADKXE001', axis=1, inplace=True)
elif parameter=='traveltime':
    df_us_copy.drop('ADLOE001', axis=1, inplace=True)
elif parameter=='transportationmeans':
    df_us_copy.drop('ADLME001', axis=1, inplace=True)

######### 
# For null model covering the entire USA
######### 
df_us_tussen=df_us_copy.copy()
df_us_tussen.drop('STATEA', axis=1, inplace=True)
#Set areal units as index
df_us_indexed=df_us_tussen.set_index(['GISJOIN'])


#Transform to dict of dicts
print 'Starting creation of dict of dicts'
dict_us=df_us_indexed.to_dict(orient='index')
print dict_us.items()[0]
print 'Ended creation of dict of dicts'

############################
#3.  Calculate representation values for data based on null model for entire USA. 

# and work out a population weighted z_score over different classes for each gisjoin
############################
'''
print 'Starting caluclation of representation values'
r_dict= mb.representation(dict_us)
print 'Ended caluclation of representation values'
'''
# mb.representation its outcome is dict of dict with 
# {areal_id: {class_id: (representation_values, variance of the null model)}}

#####################
#3.1 Convert r_dicts to pandas dataframe 
#####################
'''
def convert_r_dict_to_df(r_dict):
    r_df = pd.DataFrame([(area_id, class_id, tuple_of_r_outcomes) 
                        for area_id, dict_of_classes_and_rvalues in r_dict.items()
                        for class_id, tuple_of_r_outcomes in dict_of_classes_and_rvalues.items()
                        ])
    r_df.columns = ['area_id','class_id','tuple']
    r_df[['r_value', 'r_variance_null_model']] = r_df['tuple'].apply(pd.Series)
    r_df = r_df.drop('tuple', 1)

    return r_df
print 'Starting conversion of r_dicts to panda DataFrame'
r_df=convert_r_dict_to_df(r_dict)
print 'Ended conversion of r_dicts to panda DataFrame'
print r_df.head(10)
'''

#####################
#3.2 Add information on statistically significant over- or under representation
#####################
# Remember that the expected values for r given the null model are 1, 
# implicating that 1 +/- 2.57*stdv of null models is the confidence interval
# for 99%.  The stdv of the null models equals the square root of its variance 
'''
avg_exp_value_for_null_model = 1 #for gaussian distribution of nullmodel
confidence_interval_factor = 2.57 #for 99% interval of gaussidan distribution
'''
###############
#3.2.1 Calculate z-score for value
###############
'''
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
'''
#####################
#3.3 Save r_dataframe to pickle
#####################
'''
print 'Starting saving of r_DataFrame to pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_r_nullmodel_us.pkl' %(parameter,parameter)
picklename=foldername+filename

r_df.to_pickle(picklename)
print 'Ended saving of r_DataFrame to pickle'
'''

#####################
#3.4 Calculate one measure of segregation, weighting representation values (z-scores) with population numbers
# Remark that we work with the z-scores as the variance for each representation value is different. 

# Remark that there is probably a small problem with classes that have 0 population. Even though they might 
#have a z_score (is dat zo, krijgen ze mss gewoon NaNs?), multiplying by population 0 will make them 
#not be included in the multiplication and thus weighting performed below. This effect, however is really small.

#####################
'''
# Pivot r_df to a df with index aread_id, columns class_id values and as values, the calculated r_values
#r_df_pivot=r_df.pivot(index='area_id', columns='class_id', values='r_value').copy()

# If you don't specify values in pivot, he creates a hierarchical dataframe for all columns that are not in the pivot command
# You can thus access a pivoted table for all columns by typing r_df_pivot['columname']

# Options for r_df_all_states[columnname] are
# z_score
# r_values
# r_variance_null_model
# signif_cat_99

r_df_pivot_all_columns=r_df.pivot(index='area_id', columns='class_id').copy()

# df_us gives the amount of people per areal unit, per class.
n_df_us=df_us.set_index(['GISJOIN']).copy()

# Join on indexes
df_n_z_score=pd.merge(r_df_pivot_all_columns['z_score'],n_df_us,how='left',left_index=True, right_index=True) 

#multiply number of users per class with z_score per class for each gisjoin, and this for all classes.  
class_id_list=r_df.class_id.unique()

columns_with_z=[]
columns_with_n=[]
columns_with_populated=[]
columns_with_populated_abs=[]

for class_id in class_id_list:
	#Remark that the merge names class_id_x and class_id_y because of similar column names for n_df_us and r_df_all_state_pivot_all_columns.
	class_id_x=class_id + '_x'
	class_id_y=class_id + '_y'
	class_id_populated=class_id + '_populated_z_score'
	class_id_populated_abs=class_id + '_populated_z_score_abs'

	df_n_z_score[class_id_populated]=df_n_z_score[class_id_x]*df_n_z_score[class_id_y]
	df_n_z_score[class_id_populated_abs]=df_n_z_score[class_id_populated].abs()
	
	columns_with_z.append(str(class_id_x))
	columns_with_n.append(str(class_id_y))
	columns_with_populated.append(str(class_id_populated))
	columns_with_populated_abs.append(str(class_id_populated_abs))


df_n_z_score['abs_sum']=df_n_z_score[columns_with_populated_abs].sum(axis=1)
df_n_z_score['total_pop']=df_n_z_score[columns_with_n].sum(axis=1)
df_n_z_score['weighted_abs_z_score']=df_n_z_score['abs_sum']/df_n_z_score['total_pop']

#add population of percentages to the dataframe. 

columns_with_pop_percentage=[]

for class_id in class_id_list:
    class_id_y=class_id + '_y' # all columns from n_df_us
    class_id_pop_percentage= class_id + '_pop_percentage'
    df_n_z_score[class_id_pop_percentage]=df_n_z_score[class_id_y]/df_n_z_score[total_pop]
    columns_with_pop_percentage.append(class_id_pop_percentage)

df_n_z_score[columns_with_pop_percentage].round(2)
df_n_z_score.head(5)
'''
#####################
#3.5 Save dataframe with Z-scores, populations and weighted abs z-score to pickle
#####################
'''
print 'Starting saving of df_n_z_score to pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_n_z_weighted_z_nullmodel_us.pkl' %(parameter,parameter)
picklename=foldername+filename

df_n_z_score.to_pickle(picklename)
print 'Ended saving of df_n_z_score to pickle'
'''
############################
#5.  Calculate exposure values (repulsion-attraction matrices) for entiry country

# In marble it takes too much time; probably because of the calculation of the variance.
# Remark that Maartens implemenetation means we have not yet added significancy scores to these calculations. 
############################

#####################
#5.1 Define helper functions
#####################
'''
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
'''

#####################
#5.2.Read in r_values 
#####################
'''
#based on null model of entire country
print 'Starting reading in from pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_r_nullmodel_us.pkl' %(parameter,parameter)
picklename=foldername+filename

r_df=pd.read_pickle(picklename)
'''
#####################
#5.3 Calculate exposure values for entire country (based on null model of entire country)
#based on Maarten's implementation
# Remark that Maartens implemenetation means we have not yet added significancy scores to these calculations. 
#####################
'''
#df_us gives the amount of people per areal unit, per class. 
#df_us_sum gives the amount of people per class for the entire area
df_us_sum = df_us.sum()
#r_df gives the representation values per class and per areal unit. 

# Fill dict with exposure values
class_id_list= r_df.class_id.unique()

print 'Starting calculation of exposure values based on Maartens implementation'
exp_dict={}
for class_id in class_id_list:
    exp_dict[class_id]={}
for class_id in class_id_list:
        for class_id2 in class_id_list:
            exp_dict[class_id][class_id2]=calc_exposure(r_df,df_us,df_us_sum,'area_id','GISJOIN',class_id,class_id2)
print 'Ended calculation of exposure values based on Maartens implementation'

# Convert dict to dataframe. 
exp_df=convert_exp_dict_to_df(exp_dict)
'''
#####################
#5.4 Save exposure dataframe to pickle
#####################
'''
print 'Starting saving of exposure_DataFrame to pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_exp_nullmodel_us.pkl' %(parameter,parameter)
picklename=foldername+filename

exp_df.to_pickle(picklename)
print 'Ended saving of exposure_DataFrame to pickle'
'''




############################
#7.  Figures for representation
############################


#####################
#7.1 Read in r_dataframe from pickle
#####################
'''
print 'Starting reading in from pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_r_nullmodel_us.pkl' %(parameter,parameter)
picklename=foldername+filename

r_df=pd.read_pickle(picklename)
'''

###############
#7.2 Define outputfolder
###############E
'''
outputfolder='/Users/maarten/Desktop/nyu-code/residential_segregation/'
''' 
###############
#7.3 Show some plots of distribution of z-scores
###############E

############################  Develop these figures better. 
###########################  Also, count and investigate the occurence of nan values for the r_values.
'''
print'Saving some plots on the distribution of z_scores'
outputfile='figures_US_%s_censustracts_2015_r/distr_z-score_r_%s_us_tract_2015.png' %(parameter,parameter)
outputname=outputfolder+outputfile
r_df.hist(column='z_score', bins=50)
plt.savefig(outputname)


print'Saving some plots on the distribution of the 99 procent classes'
outputfile='figures_US_%s_censustracts_2015_r/distr_sign_cat_r_%s_us_tract_2015.png' %(parameter,parameter)
outputname=outputfolder+outputfile
r_df['signif_cat_99'].value_counts().plot(kind='bar')
plt.savefig(outputname)
'''

#####################
#7.4 Investigate spatial pattern of representation
#####################

#####################
#7.4.1 Read in geo data
#####################
'''
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
'''
#####################
#7.4.1 Join geo data and r_df
#####################
'''
print 'Joining geo data and representation values'
r_df_geo=pd.merge(r_df,df_geo_trct_small, how='left', left_on='area_id', right_on ='GISJOIN').rename(columns={'INTPTLAT': 'lat','INTPTLON': 'lon'})

# Investigate join losses. Look further to see the reasons behind. 
# r_df_geo.isnull().sum()
# for all columns (so also NaNs we have in the r_value calculations):
#r_df_geo_nans=r_df_geo[r_df_geo.isnull().any(axis=1)]
# for one columns:
r_df_geo_nans_join_column=r_df_geo[r_df_geo['GISJOIN'].isnull()]
# print 'during the join we lost ' + str(float(r_df_geo_nans.size)/float(r_df_geo_nans_join_column.size)) + ' percentage of rows'

if r_df_geo_nans_join_column.size == 0:
    print 'Join is ok'
else:
    print 'Join is not ok, we lost ' + str(float(r_df_geo_nans_join_column.size)/float(r_df_geo.size)) + ' percentage of rows'
'''

#############
#7.4.2 Scatter map for z-scores (continous)
#############
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
'''
#############
#7.4.3 Scatter for significant test (categorical)
#############
'''
print 'Starting the creation of maps for 99 procent classes of representation values'
# Get list of unique classes
class_id_list= r_df_geo.class_id.unique()

for class_id_name in class_id_list:

    df_one_class=r_df_geo.loc[r_df_geo['class_id'] == class_id_name]

    colors = {'or':'red', 'ur':'blue', 'ns':'grey'}

    fig, ax1=plt.subplots(figsize=(18,12))
    sc=ax1.scatter(df_one_class['lon'],df_one_class['lat'], c=df_one_class['signif_cat_99'].apply(lambda x: colors[x]),s=1,alpha=0.5)
    title_name='Significance of representativity values for class %s in %s' %(class_id_name,parameter)
    ax1.set_title(title_name,fontsize=11) 

    #ax1.autoscale_view()
    ax1.margins(0.1) # Margins to the side of the figure
    # To not show alaska, puerto rico and other weird territories
    ax1.set_xlim(-130,-65)
    ax1.set_ylim(24,50)

############################  Work out a proper legend. 
    #plt.show()

    figname = 'figures_US_%s_censustracts_2015_r/map_sign_cat_r_%s_%s_us_tract_2015.png' %(parameter,parameter,class_id_name)
    outputname=outputfolder+figname
    plt.savefig(outputname)
    plt.clf()
    plt.close('all')

print 'Ended the creation of maps for 99 procent classes of representation values'    
'''




############################
#7.  Figures for rexposure (Hinton diagrams)
############################


#####################
#7.1 Read in exp_dataframe from pickle
#####################
'''
print 'Starting reading in from pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_exp_nullmodel_us.pkl' %(parameter,parameter)
picklename=foldername+filename

exp_df=pd.read_pickle(picklename)
'''
#####################
#7.2 Make and save hinton figure
#####################
'''
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
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,facecolor=color, edgecolor=color)
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

print 'Started creating hinton diagram'
#Put data in right format
exp_df_for_hinton = exp_df.pivot(index='class_id1', columns='class_id2', values='exp_value')

#Create, show or save hinton
hinton(exp_df_for_hinton)
title_name= 'Hinton diagram of exposure values for %s classes in the US.png' %parameter
plt.title(title_name)

#plt.show()

outputfolder='/Users/maarten/Desktop/nyu-code/residential_segregation/'
figname = 'figures_US_%s_censustracts_2015_r/hinton_diagram_exp_%s_us_tract_2015.png' %(parameter,parameter)
outputname=outputfolder+figname
plt.savefig(outputname)
plt.close("all")
print 'Ended creating hinton diagram'
'''
