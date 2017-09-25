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
import marble as mb


############################
#1. Read in data
############################

#####################
#1.1 Define inputfiles
#####################

foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/'

filename_income ='income_blockgroup_ny_2011_2015/nhgis0005_ds215_20155_2015_blck_grp.csv'
filename_race = 'race_blockgroup_ny_2011_2015/nhgis0004_ds215_20155_2015_blck_grp.csv'
filename_traveltime = 'traveltime_blockgroup_ny_2011_2015/nhgis0006_ds215_20155_2015_blck_grp.csv'

inputfile_income = foldername+filename_income
inputfile_race = foldername+filename_race
inputfile_traveltime = foldername+filename_traveltime

#####################
#1.2 Read in OD files
#####################

df_income_ny_full = pd.read_csv(inputfile_income, sep=',', lineterminator='\n')
print df_income_ny_full.head(10)

df_race_ny_full = pd.read_csv(inputfile_race, sep=',', lineterminator='\n')
print df_race_ny_full.head(10)

df_traveltime_ny_full = pd.read_csv(inputfile_traveltime, sep=',', lineterminator='\n')
print df_traveltime_ny_full.head(10)

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

df_income_ny=df_income_ny_full[
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

df_race_ny=df_race_ny_full[
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

df_traveltime_ny=df_traveltime_ny_full[
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

#print df_income_ny.head(10)
#print df_race_ny.head(10)
#print df_traveltime_ny.head(10)


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

df_income_ny.drop('ADNJE001', axis=1, inplace=True)
df_race_ny.drop('ADKXE001', axis=1, inplace=True)
df_traveltime_ny.drop('ADLOE001', axis=1, inplace=True)

#Set areal units as index
df_income_ny_indexed=df_income_ny.set_index(['GISJOIN'])
df_race_ny_indexed=df_race_ny.set_index(['GISJOIN'])
df_traveltime_ny_indexed=df_traveltime_ny.set_index(['GISJOIN'])


print df_income_ny_indexed.head()
print df_race_ny_indexed.head()
print df_traveltime_ny_indexed.head()

#Transform to dict of dicts
income_ny_dict=df_income_ny_indexed.to_dict(orient='index')
race_ny_dict=df_race_ny_indexed.to_dict(orient='index')
traveltime_ny_dict=df_traveltime_ny_indexed.to_dict(orient='index')

print income_ny_dict.items()[0]
print race_ny_dict.items()[0]
print traveltime_ny_dict.items()[0]



############################
#3.  Calculate representation values for data. 
############################

r_income= mb.representation(income_ny_dict)
r_race= mb.representation(race_ny_dict)
r_traveltime= mb.representation(traveltime_ny_dict)

# mb.representation its outcome is dict of dict with 
# {areal_id: {class_id: (representation_values, variance of the null model)}}


#####################
#3.1 Add informaion on statistically significant over- or under representation

# Remember that the expected values for r given the null model are 1, 
# implicating that 1 +/- 2.57*stdv of null models is the confidence interval
# for 99%.  The stdv of the null models equals the square root of its variance 
#####################


# Remark from Maarten, it will be more elegant to compare the z-scores to a value rather than calculating the boundaries of the confidence interval, but ok.

def r_add_signif(r_input, expected_value=1, confidence_interval_factor=2.57):
    '''
    expected_value = 1 #for gaussian distribution of nullmodel
    confidence_interval_factor = 2.57 #for 99% interval of gaussidan distribution

    ns= non-significant
    ur= signiifcantly under-represented
    or= significantly over-represented
    '''

    # make a copy so you don't mess with the original dict
    import copy
    r_outcome = copy.deepcopy(r_input) 

    for area_id, dict_of_classes_and_rvalues in r_outcome.items():
        for class_id, r_tuple in dict_of_classes_and_rvalues.items():

            #calculate z-score with relation to null model which has mean=expected value
            z_score = (r_tuple[0]-expected_value)/pow(r_tuple[1],0.5)

            #setup boundaries of confidence interval
            upper_bound=expected_value + (confidence_interval_factor*pow(r_tuple[1],0.5))
            lower_bound=expected_value - (confidence_interval_factor*pow(r_tuple[1],0.5))

            #print 'observed value is ' + str(r_tuple[0]) + ' while boundaries of confidence interval are ' + str((lower_bound,upper_bound)) + ' hence we find this value to be ' 
            if r_tuple[0] < lower_bound:
                #print 'significantly under-represented'
                r_outcome[area_id][class_id]=(r_tuple[0],r_tuple[1],z_score,'ur')
                

            elif r_tuple[0] > upper_bound:
                #print 'significantly over-represented'
                r_outcome[area_id][class_id]=(r_tuple[0],r_tuple[1],z_score,'or')

            else: 
                #print 'non-significant'
                r_outcome[area_id][class_id]=(r_tuple[0],r_tuple[1],z_score,'ns')

    return r_outcome

r_income_signif= r_add_signif(r_income)
r_race_signif= r_add_signif(r_race)
r_traveltime_signif= r_add_signif(r_traveltime)


############
#3.1.1 Investigate the amount of underrepresented and overrepresented per class_id
############

# Recreate pandas dataframe from r_dicts.
r_income_signif_pandas = pd.DataFrame([(area_id, class_id, tuple_of_r_outcomes) 
                                        for area_id, dict_of_classes_and_rvalues in r_income_signif.items()
                                        for class_id, tuple_of_r_outcomes in dict_of_classes_and_rvalues.items()
                                        ])
r_income_signif_pandas.columns = ['area_id','class_id','tuple']
r_income_signif_pandas[['r_value', 'r_variance','z_score','signif_cat_99']] = r_income_signif_pandas['tuple'].apply(pd.Series)

r_race_signif_pandas = pd.DataFrame([(area_id, class_id, tuple_of_r_outcomes) 
                                        for area_id, dict_of_classes_and_rvalues in r_race_signif.items()
                                        for class_id, tuple_of_r_outcomes in dict_of_classes_and_rvalues.items()
                                        ])
r_race_signif_pandas.columns = ['area_id','class_id','tuple']
r_race_signif_pandas[['r_value', 'r_variance','z_score','signif_cat_99']] = r_race_signif_pandas['tuple'].apply(pd.Series)

r_traveltime_signif_pandas = pd.DataFrame([(area_id, class_id, tuple_of_r_outcomes) 
                                        for area_id, dict_of_classes_and_rvalues in r_traveltime_signif.items()
                                        for class_id, tuple_of_r_outcomes in dict_of_classes_and_rvalues.items()
                                        ])
r_traveltime_signif_pandas.columns = ['area_id','class_id','tuple']
r_traveltime_signif_pandas[['r_value', 'r_variance','z_score','signif_cat_99']] = r_traveltime_signif_pandas['tuple'].apply(pd.Series)


print r_income_signif_pandas.head(3)
print r_race_signif_pandas.head(3)
print r_traveltime_signif_pandas.head(3)



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



'''

