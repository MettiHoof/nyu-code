Some meta-information on the LODES data that we will predominantly use:

- The source of the data is: https://lehd.ces.census.gov/data/lodes/LODES7/

- Combines both the main (od's within the state borders) and aux (od's over state borders with work in state and home out of state (so no double counts) datasets for all states

- Uses the JT00 segment (all users), there is additional segmentation possible for three classes in age, earnings and sector.

- Has the S000 variable (total commuting persons), there exists a segmentation based on the type of jobs (private vs public sector etc.) but i omitted this information to keep the file smaller.

- The data is gathered in 2015

- Is aggregated at the census tract level. Strangely, the census tract delineation that has been used in this data from 2015 is the 2010 census tract delineation.

- Data is filtered on at least 10 commuting persons. This significantly reduces the size of the dataset.

