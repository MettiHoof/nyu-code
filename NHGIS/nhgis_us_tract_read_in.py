##############################################################################################

# Performing residential segregation analysis on census data at tract level for the USA - nhgis. 

# Script writtne by Maarten on 10/10/2017

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

########
# For null model covering each state separately
######### 

df_us_tussen2=df_us_copy.copy()
state_list= df_us_tussen2.STATEA.unique()
# We create a dict with as key, the statename and as element the dict that we need 
# to feed into marble to make it work. 

print 'Started filling the dict by state'
dict_by_state={}

for state in state_list:
    df_state=df_us_tussen2.loc[df_us_tussen2['STATEA'] == state].copy()
    df_state.drop('STATEA', axis=1, inplace=True) 
    df_state_indexed=df_state.set_index(['GISJOIN'])
    dict_state=df_state_indexed.to_dict(orient='index')
    dict_by_state[state]=dict_state 

#dict_by_state['01']['G0101250011401']['ADKXE008']
print 'Ended filling the dict by state'

