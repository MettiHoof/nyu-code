##############################################################################################
# Script to analyse the relation between populations and z-scores 

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
import marble as mb
import copy

# Parameter to define which classes we are going to work with. 
parameter='race' #income, race, traveltime, transportationmeans


############################
#6.  Analysis of the relation between r-values and initial populations, and aggregated Z_scores 
############################
#####################
#6.1 Read in the df_n_zscore_all_states dataframe 
#####################

print 'Start loading of df_n_zscore_all_states from pickle'
foldername ='/Users/maarten/Desktop/nyu-data/NHGIS/us/'
filename= '%s_censustracts_us_2015/%s_censustracts_us_2015_pickle_n_z_weighted_z_nullmodel_perstate.pkl' %(parameter,parameter)
picklename=foldername+filename

df_n_z=pd.read_pickle(picklename)

print 'Ended loading of df_n_zscore_all_states from pickle'


#####################
#6.2 Set up the different subclasses that are in the dataframe 
#####################

z_score_cols = [col for col in df_n_z.columns if '_z_score' in col]
n_cols = [col for col in df_n_z.columns if '_pop' in col]
z_cols = [col for col in df_n_z.columns if '_populated_z_score' in col[-17:]]
z_abs_cols = [col for col in df_n_z.columns if '_populated_z_score_abs' in col]
n_perc_cols=[col for col in df_n_z.columns if '_pop_percentage' in col]


#####################
#6.3 Set outputfolder 
#####################

#####################
#6.4 Explore the relation between pop_percentage of all categories and weighted abs z_score
#####################

#####################
#6.4.1 Enkelvoudige regressie (correlatie hier)
#####################
tussen= copy.copy(n_perc_cols)
tussen.append('weighted_abs_z_score')
tussen.append('total_pop')
df_tussen=df_n_z[tussen]
corrs=df_tussen.corr()
print corrs['weighted_abs_z_score']

'''
for cat in n_perc_cols:
    df_n_z.plot(x=[cat], y='weighted_abs_z_score', style='o')
    plt.show()
    plt.close('all')
'''

#####################
#6.4.2.1 Meervoudige Regressie for all variables
#####################
'''
import statsmodels.api as sm

# slice part of the data you need 
tussen= copy.copy(n_perc_cols)
tussen.append('weighted_abs_z_score')
df_tussen=df_n_z[tussen]
#make a copy; filter out nans
df_ols=df_tussen.copy()
print df_ols.shape
df_ols_nona=df_ols.dropna()     #drop all rows that have any NaN values
print df_ols_nona.shape

#Set up dependent and independent variables
X= df_ols_nona[n_perc_cols]
y =df_ols_nona['weighted_abs_z_score']

#Estimate model
est = sm.OLS(y, X).fit()
#print summary
est.summary()

'''
#####################
#6.4.2.2 Meervoudige Regressie and 3D plot for 2 variables zonder interactie
#####################
'''
from mpl_toolkits.mplot3d import Axes3D

x_var1='ADKXE002_pop_percentage'
x_var2='ADKXE003_pop_percentage'
two_variables=[x_var1,x_var2]
y_name='weighted_abs_z_score'

#Set up dependent and independent variables
X= df_ols_nona[two_variables]
y =df_ols_nona[y_name]
#Force an intercept on the X variables. 
X = sm.add_constant(X)


#Estimate model without interaction
est = sm.OLS(y, X).fit()
#print summary
est.summary()

#Fit 3d plot for 3 variables. 
# The damned X.x moet hardcoded zijn. moeder.  
xx1, xx2 = np.meshgrid(np.linspace(X.ADKXE002_pop_percentage.min(), X.ADKXE002_pop_percentage.max(), 100), 
                       np.linspace(X.ADKXE003_pop_percentage.min(), X.ADKXE003_pop_percentage.max(), 100)) 
# plot the hyperplane by evaluating the parameters on the grid
Z = est.params[0] + est.params[1] * xx1 + est.params[2] * xx2

# create matplotlib 3d axes
fig = plt.figure(figsize=(18, 10))
ax = Axes3D(fig, azim=-115, elev=15)

# plot hyperplane
surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

# plot data points - points over the HP are white, points below are black
resid = y - est.predict(X)
ax.scatter(X[resid >= 0].ADKXE002_pop_percentage, X[resid >= 0].ADKXE003_pop_percentage, y[resid >= 0], color='black', alpha=1.0, facecolor='white')
ax.scatter(X[resid < 0].ADKXE002_pop_percentage, X[resid < 0].ADKXE003_pop_percentage, y[resid < 0], color='black', alpha=1.0)

# set axis labels
ax.set_xlabel(x_var1)
ax.set_ylabel(x_var2)
ax.set_zlabel(y_name)

plt.show()
plt.close('all')
'''
#####################
#6.4.2.2 Meervoudige Regressie and 3D plot for 2 variables met interactie
#####################
'''
import statsmodels.formula.api as smf
from mpl_toolkits.mplot3d import Axes3D

x_var1='ADKXE002_pop_percentage'
x_var2='ADKXE003_pop_percentage'
y_var='weighted_abs_z_score'

#Estimate model with interaction
est = smf.ols(formula='weighted_abs_z_score ~ ADKXE002_pop_percentage * ADKXE003_pop_percentage', data=df_ols_nona).fit() 
#print summary
est.summary()
est.params

#Fit 3d plot for 3 variables. 
# The damned X.x moet hardcoded zijn. moeder.  
xx1, xx2 = np.meshgrid(np.linspace(X.ADKXE002_pop_percentage.min(), X.ADKXE002_pop_percentage.max(), 100), 
                       np.linspace(X.ADKXE003_pop_percentage.min(), X.ADKXE003_pop_percentage.max(), 100)) 
# plot the hyperplane by evaluating the parameters on the grid
Z = est.params[0] + est.params[1] * xx1 + est.params[2] * xx2 + est.params[3] *xx1 * xx2

# create matplotlib 3d axes
fig = plt.figure(figsize=(18, 10))
ax = Axes3D(fig, azim=-115, elev=15)

# plot hyperplane
surf = ax.plot_surface(xx1, xx2, Z, cmap=plt.cm.RdBu_r, alpha=0.6, linewidth=0)

# plot data points - points over the HP are white, points below are black
resid = y - est.predict(X)
ax.scatter(X[resid >= 0].ADKXE002_pop_percentage, X[resid >= 0].ADKXE003_pop_percentage, y[resid >= 0], color='black', alpha=1.0, facecolor='white')
ax.scatter(X[resid < 0].ADKXE002_pop_percentage, X[resid < 0].ADKXE003_pop_percentage, y[resid < 0], color='black', alpha=1.0)

# set axis labels
ax.set_xlabel(x_var1)
ax.set_ylabel(x_var2)
ax.set_zlabel(y_var)

plt.show()
plt.close('all')
'''