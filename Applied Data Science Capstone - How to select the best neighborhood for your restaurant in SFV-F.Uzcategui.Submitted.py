#!/usr/bin/env python
# coding: utf-8

# <h1>Applied Data Science Capstone : How to select the best neighborhood for your restaurant in San Fernando Valley? </h1>
# 
# <h3>Autor: Francihelena Uzcategui</h3>
# 
# ## Table of Contents
# 
# <ul>
# <li><a href="#wrangling">I.Introduction
# <li><a href="#wrangling">II.Data   
# <li><a href="#wrangling">1. Data Wrangling: 1.1, 1.2, and 1.3</a></li>
# <li><a href="#cleaning">2. Data Cleaning: 2.1 , 2.2, and 2.3</a></li>
# <li><a href="#methodology">III.Methodology
# <li><a href="#eda">3. Exploratory Data Analysis: 3.1, 3.2, and 3.3 </a></li>
# <li><a href="#eda">4. Getting the latitude and the longitude coordinates of each neighborhood</a>
# <li><a href="#eda">5. Explore Los Angeles county, Los Angeles city and San Fernando Valley </a></li>
# <li><a href="#eda">5.1 Foursquare API to explore the San Fernando Valley neighborhoods and segment them </a></li>
# <li><a href="#eda">6. Explore Neighborhoods in San Fernando Valley</a></li>
# <li><a href="#eda">7. Analyze each neighborhoods of San Fernando Valley</a></li>
# <li><a href="#eda">8. Machine Learning Algorithms</a></li>
# <li><a href="#eda">8.1 Clusters in San Fernando Valley neighborhoods</a></li>
# <li><a href="#results">IV.Results    
# <li><a href="#eda">9. Examine Clusters of San Fernando Valley</a></li>
# <li><a href="#eda"> V. Discussion</a></li>
# <li><a href="#eda"> VI. Conclusion</a></li>
# <li><a href="#eda"> 10. Limitations</a></li>
# </ul>
# 
# 
# ##  I. Introduction
# 
# <p>A client is looking to open a casual restaurant in San Fernando Valley, California.
# The San Fernando Valley is an urbanized valley in Los Angeles County, California [1]. 
# Nearly two-thirds of the Valley's land area is part of the city of Los Angeles.
# The Valley as well called, is surrounded by many touristic and iconic places of Los Angeles city and Los Angeles county. 
# For example, San Fernando Valley is 18 miles north of Downtown Los Angeles. It is also about 17  miles from Santa Monica beach. These are just two of the numerous iconic's locations close to the Valley.
# Also, the entertainment industry's headquartered are here, such a Disney, Warner Bros., Universal Studios, Dreamworks Animation, Cartoon Network, and Motion Picture Association of America. 
# In the last years, doing business in the San Fernando Valley has been going flexibly. Its cities earned this reputation, being a stimulus to the economic growth of the region [2].  Thus, it is going to be promissory and prosper launch a new business here, in your case, a Restaurant.</p>
# 
# <p>For this analysis, we require data of the borough, neighborhood, ZIP Code, longitude, and latitude. But, the county of Los Angeles does not have boroughs; it has unincorporated communities, incorporated cities, and neighborhoods of the city of Los Angeles - such as San Fernando Valley.
# Thus, to deal with the lack of boroughs, we defined two categories San Fernando Valley and Los Angeles. The map below shows San Fernando Valley, our target.</p>
# 
# ![alt text](SFV_MAP.png "MAP")
# <p><center>Source: http://maps.latimes.com/neighborhoods/region/san-fernando-valley/</center></p>
# 
# 
# Data used:
# 1. Congressional Districts Los Angeles County - By Zip Code --> To get zip codes by districs. For the sake of the data management, this link shows the zip codes and communities compacted, without losing information or sense.
# Source: http://www.laalmanac.com/government/gu02a.php
# 
# 2. Los Angeles Zip Codes --> Getting the latitude and the longitude coordinates of each neighborhood in Los Angeles county. 
# Source: https://data.lacounty.gov/GIS-Data/ZIP-Codes-and-Postal-Cities/wft9-k7e3
# 
# 3. San Fernando Valley (target region) : Incorporated/Uncorporated cities and City of Los Angeles neighborhoods --> Target data.
# Source : https://en.wikipedia.org/wiki/San_Fernando_Valley
# 
# Thus, with these three sets of information, we built a dataset with 5 columns: region, neighborhood, ZIP code, longitude, and latitude.
#  
# To wrangle the data, we required to scrape the Wikipedia page and official pages, then cleaning it, joining between them, and creating a structured data frame.
# 
# Once the data is in a structured format, we explored, visualized, segmented, and clustered the neighborhoods by the region of San Fernando Valley.

# <p>Source:
# [1] https://en.wikipedia.org/wiki/San_Fernando_Valley, 
# [2] https://laedc.org/wtc/chooselacounty/regions-of-la-county/san-fernando-valley/</p>

# Download all the dependencies that we will need

# In[1]:


import matplotlib.pyplot as plt
from pywaffle import Waffle

import emoji

from functools import reduce

import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system("conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab")
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

#!conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab
import folium # map rendering library

print('Libraries imported.')


# ## II. Data : 1. Data Wrangling
# ## *1.1 First Data : Congressional Districts Los Angeles County - By Zip Code*

# Source:<a> http://www.laalmanac.com/government/gu02a.php</a> --> Direct dowloaded from the web page to Excel
# <p>We selected this data because of many zip code areas are split among two or more communities, being similar to the Borough organization to NYC or Toronto (previous exercise). </p>

# In[2]:


df1= pd.read_excel("C:/Users/Franchi/Documents/IBM/8th course_Applied Data Sciences Capstone Project/2nd project/data/Congressional Districts.LA COUNTY and Zip Codes.xlsx")
df1.head()


# We selected only Los Angeles, and it's communities or neighborhoods. 

# ## II. Data : 2. Data Cleaning
# ## *2.1 First Data : Congressional Districts Los Angeles County - By Zip Code*

# In[3]:


df1= df1[df1['Zip Code – City/Community'].str.contains('Los Angeles')]
df1.head()


# Removing unwanted columns

# In[4]:


df1= df1.drop(['District(s)'],axis=1)
df1.head()


# Splitting 'Zip Code – City/Community' column to obtain two columns, one for Zip Code and another for City/Community, this last one requires more splitting(more steps below). Then renaming the columns.  

# In[5]:


df1= df1['Zip Code – City/Community'].str.split("-", n=1, expand=True)
df1.columns = ["ZIP Code", "City/Community"] #renaming columns, but the .rename is not working
df1.head()


# <p>With the next splitting process, we cannot keep the ZIP Code column, but we require it, and we'll recover it by inner join, in the following steps. Thus, creating a new column index1 will be the matching criterion with the next data frame df2.<p/>

# In[6]:


df1['index1'] = df1.index
df1.head()


# Splitting 'City/Community' column to separate Los Angeles city from it's communities. Then renaming the columns

# In[7]:


df2=df1["City/Community"].str.split("(", n=1, expand=True)  
df2.columns = ["City","Community"] 
df2.head()


# To remove unwanted characters as the parenthesis )

# In[8]:


df2['Community']=df2['Community'].str.replace(r")"," ")
df2.head()


# Creating a new column 'index2', that have common values with the previous data frame df1['index1'], to apply the inner join.

# In[9]:


df2['index2'] = df2.index
df2.head()


# Applying inner join for the two data frames: df with df2, to consolidate into one data frame the ZIP Code, City, and Community.

# In[10]:


df3=df1.join(df2.set_index('index2'), on='index1', how='inner')
df3.head()


# Dropping unwanted column "index1"

# In[11]:


df3 = df3.drop(["City/Community","index1"], axis=1)
df3.head()


# ## III. Methodology : 3. Exploratory Data Analysis
# 
# ## *3.1 First Data : Congressional Districts Los Angeles County - By Zip Code*
# 

# Checking the data frame structure and data type

# In[12]:


df3.shape


# In[13]:


df3.isnull().sum(axis = 0)


# In[14]:


df3.dtypes


# Converting data type of ZIP Code column to avoid future error on the join method. Then, verify that the data type changed.

# In[15]:


df3['ZIP Code']=df3['ZIP Code'].astype(int)
df3.dtypes


# In[16]:


print(emoji.emojize(':pushpin: Voila! Above the ready First dataset(df3) with the structure format wanted --> Community: South Los Angeles , Florence-Graham. Several communities by each zip code'))


# ## II. Data : 1. Data Wrangling 
# ## *1.2 Second Data : Los Angeles Zip Codes and Latitude/Longitude by each neighborhood in Los Angeles county*
# <p>Source: https://data.lacounty.gov/GIS-Data/ZIP-Codes-and-Postal-Cities/wft9-k7e3 --> Direct dowloaded from the web page to Excel</p>
# 
# <p>Getting the latitude and the longitude coordinates of each neighborhood </p>

# In[17]:


df4=pd.read_csv("C:/Users/Franchi/Documents/IBM/8th course_Applied Data Sciences Capstone Project/2nd project/ZIP_Codes_and_Postal_Cities.DataLAcounty.csv")
df4.head()


# ## II. Data : 2. Data Cleaning
# ## *2.2 Second Data : Los Angeles Zip Codes and Latitude/Longitude by each neighborhood in Los Angeles county*

# Dropping unwanted columns

# In[18]:


df4=df4.drop(['Postal City 2','Postal City 3','Not Acceptable 1','Not Acceptable 2','Not Acceptable 3'], axis=1)
#df=df.drop([0,0])
df4=df4.rename(columns={"Postal City 1": "Neighborhoods"})
df4.head()


# Location column mixed information, and it contains the geographic coordinates and zip codes in the same row. Thus, it should be fixed by splitting the values and then erasing the duplicate zip codes.

# In[19]:


df4[['zipcode-duplicate','Latitude','Longitude']] =df4.Location.str.split(expand=True,) #https://cmdlinetips.com/2018/11/how-to-split-a-text-column-in-pandas/
df4.head()


# Dropping duplicates columns 

# In[20]:


df4=df4.drop(['Location','zipcode-duplicate'], axis=1)
df4['Latitude']=df4['Latitude'].str.replace(r","," ")
df4.head()


# ## III. Methodology : 3. Exploratory Data Analysis
# ## *3.2 Second Data : Los Angeles Zip Codes and Latitude/Longitude by each neighborhood in Los Angeles county*

# Checking shape

# In[21]:


df4.shape


# Checking null values

# In[22]:


df4.isnull().sum(axis = 0)


# In[23]:


df4.dtypes


# In[24]:


print(emoji.emojize(':pushpin: Voila! Above is the ready Second dataset(df4) with the structure format wanted --> Columns: ZIP Code, Neighborhoods, Latitude, Longitude'))


# <p>Joining the two dataframes df3 and df4 to create a consolidated data frame with the required information:</p>
#     <p> - Columns: ZIP Code, Latitude, Longitude, City, and Community</p>
#     <p> - Several communities by each zip code</p>

# In[25]:


df_LA=df4.join(df3.set_index('ZIP Code'), on='ZIP Code', how='inner')
pd.set_option('display.max_rows', None)
df_LA#.head()


# Dropping unwanted column - Neighborhoods, because it contains general and duplicate information. Thus, we kept the Community column because it has more details of the neighborhoods and the format required.

# In[26]:


df_LA=df_LA.drop(['Neighborhoods'], axis=1)
df_LA.head()


# In[27]:


df_LA.shape


# Checking null values

# In[28]:


df_LA.isnull().sum(axis = 0)


# Dropping null values and verifying it

# In[29]:


df_LA = df_LA.dropna()
df_LA.isnull().sum(axis = 0)


# In[30]:


print(emoji.emojize(':pushpin: Voila! Above the ready Third dataset (df_LA) with the structure format required--> Columns: ZIP Code,  Latitude, Longitude, City, Community'))


# As we mentioned in the Introduction section, our target is the San Fernando Valley rather than Los Angeles city; remember that San Fernando Valley is a conglomerated of towns within Los Angeles County. Hence, we already have a list with all the communities in San Fernando Valley, and it will join to the data frame df_LA.

# ## II. Data : 1. Data Wrangling
# ## *1.3 Third Data : San Fernando Valley --> Target data*
# Source: Municipalities and neighborhoods - <a> https://en.wikipedia.org/wiki/San_Fernando_Valley</a>

# In[31]:


df5=pd.read_excel("C:/Users/Franchi/Documents/IBM/8th course_Applied Data Sciences Capstone Project/2nd project/data/San Fernado Valley -  Municipalities and neighborhoods.xlsx")
df5=df5.rename(columns={"Municipalities and neighborhoods": "Place"})
df5.head()


# ## II. Data : 2. Data Cleaning
# ## *2.3 Third Data : San Fernando Valley --> Target data*

# Convert data frame to list to then search these words within the data frame df_LA

# In[32]:


list_of_SFV_communities = df5['Place'].to_list()
list_of_SFV_communities


# Searching the list of words within the data frame, to get True or False values.

# In[33]:


#How to test if a string contains one of the substrings in a list, in pandas?
#Source: https://stackoverflow.com/questions/26577516/how-to-test-if-a-string-contains-one-of-the-substrings-in-a-list-in-pandas- Answer for Grant Shannon 

df_LA["TrueFalse"] = df_LA['Community'].apply(lambda x: 1 if any(i in x for i in list_of_SFV_communities) else 0)


# In[34]:


df_LA


# Re defining the values of True or False. Next, creating a new column with these new values.

# In[35]:


#Add new column based on boolean values in a different column
#Source:https://stackoverflow.com/questions/25570147/add-new-column-based-on-boolean-values-in-a-different-column/25570219 - Answer for EdChum 
temp = {True:'San Fernando Valley', False:'Los Angeles'}
df_LA['Cityy'] = df_LA['TrueFalse'].map(temp)
df_LA


# Dropping unwanted columns

# In[36]:


df_LA = df_LA.drop(['City', 'TrueFalse'], axis=1)
df_LA.head()


# Renaming a column

# In[37]:


df_LA = df_LA.rename(columns={'Cityy':'Region'})
df_LA.head()


# ## III.Methodology : 3 Exploratory Data Analysis
# ## *3.3 Third Data : San Fernando Valley --> Target data*

# Checking the dataframe structure

# In[38]:


df_LA.shape


# In[39]:


df_LA.dtypes


# In[40]:


df_LA.isnull().sum()


# ## 4. Getting the latitude and the longitude coordinates of each neighborhood

# In[41]:


print(emoji.emojize(':pushpin: Voila! Above the data frame (df_LA) has the latitude and the longitude coordinates of each neighborhood In Los Angeles County, including San Fernando Valley.'))


# In[42]:


df_LA.head()


# ## 5. Explore Los Angeles county,  Los Angeles city and San Fernando Valley. 
# 

# First, we processed **Los Angeles county** (whole dataset) and visualized its geographic coordinates.

# In[43]:


address = 'Los Angeles, CA'

geolocator = Nominatim(user_agent="LA_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Los Angeles are {}, {}.'.format(latitude, longitude))


# In[44]:


# create map of New York using latitude and longitude values
map_LA = folium.Map(location=[34.0536909, -118.2427666], zoom_start=10)

# add markers to map
for lat, lng, region, community in zip(df_LA['Latitude'], df_LA['Longitude'], df_LA['Region'], df_LA['Community']):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        fill_color='#3186cc',
        fill_opacity=0.7).add_to(map_LA)  
    
map_LA


# Then, processing **San Fernando Valley** and visualized its geographic coordinates

# In[45]:


SFV_data = df_LA[df_LA['Region'] == 'San Fernando Valley'].reset_index(drop=True)
SFV_data.head()


# In[46]:


SFV_data.dtypes


# In[47]:


address = 'San Fernando Valley, CA'

geolocator = Nominatim(user_agent="San Fernando Valley_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geographical coordinate of San Fernando Valley are {}, {}.'.format(latitude, longitude))


# In[48]:


# create map of San fernado Valley using latitude and longitude values
map_SFV = folium.Map(location=[34.2148853, -118.4998204], zoom_start=11)

# add markers to map
for lat, lng, region, community in zip(SFV_data['Latitude'], SFV_data['Longitude'], SFV_data['Region'], SFV_data['Community']):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        fill_color='#3186cc',
        fill_opacity=0.7).add_to(map_SFV)  
    
map_SFV


# Next, processing **Los Angeles City** and visualized its geographic coordinates

# To avoid mess up with too many cities, we defined two categories to analyze; our Target: San Fernando Valley, and, the Not target: =! San Fernando Valley. 

# In[49]:


LA_City_data = df_LA[df_LA['Region'] != 'San Fernando Valley'].reset_index(drop=True) # if use == 'los Angeles' is empty
LA_City_data.head()


# In[50]:


address = 'Los Angeles city, CA'

geolocator = Nominatim(user_agent="LA_City_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Los Angeles city are {}, {}.'.format(latitude, longitude))


# In[51]:


# create map of East Toronto using latitude and longitude values
map_LA_City = folium.Map(location=[34.0536909, -118.2427666], zoom_start=11)

# add markers to map
for lat, lng, region, community in zip(LA_City_data['Latitude'], LA_City_data['Longitude'], LA_City_data['Region'], LA_City_data['Community']):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        fill_color='#3186cc',
        fill_opacity=0.7).add_to(map_LA_City)  
    
map_LA_City


# <h3>5.1 Foursquare API to explore the San Fernando Valley neighborhoods and segment them</h3>
#     
# <p> Define Foursquare Credentials and Version</p> 
# 
# Remember that San Fernando Valley is our target

# In[52]:


CLIENT_ID = 'STODIITDYK4OHL2CWWSGTGUDWEEUYQH1RLWIRCD4CT3MGZP4'#'your-client-ID' # your Foursquare ID
CLIENT_SECRET = 'JJCMU1YNWJRADLOAMADR0V4NRGE45RRU0O0T0XBRRYCDQNYZ' #'your-client-secret' # your Foursquare Secret
VERSION = '20180605' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# ## 6. Explore Neighborhoods in San Fernando Valley 

# In[53]:


def getNearbyVenues(names, latitudes, longitudes, radius=500, LIMIT=100):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Community', 
                  'Community Latitude', 
                  'Community Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# Now write the code to run the above function on each neighborhood and create a new data frame called SFV_venues. SFV is the acronym of San Fernando Valley.

# In[54]:


SFV_venues = getNearbyVenues(names=SFV_data['Community'],
                                   latitudes=SFV_data['Latitude'],
                                   longitudes=SFV_data['Longitude']
                                  )


# In[55]:


print(SFV_venues.shape)
SFV_venues.head()


# ## 7. Analyze each neighborhood of San Fernando Valley

# In[56]:


SFV_venues.groupby('Community').count()


# In[57]:


print('There are {} uniques categories.'.format(len(SFV_venues['Venue Category'].unique())))


# In[58]:


# one hot encoding
SFV_onehot = pd.get_dummies(SFV_venues[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
SFV_onehot['Community'] = SFV_venues['Community'] 

# move neighborhood column to the first column
fixed_columns = [SFV_onehot.columns[-1]] + list(SFV_onehot.columns[:-1])
SFV_onehot = SFV_onehot[fixed_columns]

SFV_onehot.head()


# In[59]:


#And let's examine the new dataframe size
SFV_onehot.shape


# Grouping rows by neighborhood and by taking the mean of the frequency of occurrence of each category

# In[60]:


SFV_grouped = SFV_onehot.groupby('Community').mean().reset_index()
SFV_grouped


# In[61]:


#confirm the new size
SFV_grouped.shape


# Writing a function to sort the venues in descending order.

# In[62]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# Creating the new data frame and displaying each neighborhood with the top 10 most common venues

# In[63]:


num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Community']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
community_venues_sorted = pd.DataFrame(columns=columns)
community_venues_sorted['Community'] = SFV_grouped['Community']

for ind in np.arange(SFV_grouped.shape[0]):
    community_venues_sorted.iloc[ind, 1:] = return_most_common_venues(SFV_grouped.iloc[ind, :], num_top_venues)

community_venues_sorted.head()


# ## 8. Machine Learning Algorithms
# 
# Community venues dataset has two dimensions, the typical venues, and the communities. Furthermore, finding common patterns is a simple and efficient way to deal with it. K - means algorithms help to cluster these features. We set the number of clusters: two. This algorithm looks for similar group venues within each neighborhood of San Fernando Valley.

# <h2> 8.1 Clusters in San Fernando Valley neighborhoods</h2>

# In[64]:


#Run k-means to cluster the neighborhood into 2 clusters.

# set number of clusters
kclusters = 2

SFV_grouped_clustering = SFV_grouped.drop('Community', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(SFV_grouped_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 


# Let's create a new data frame that includes the clusters and the top 10 venues for each neighborhood.

# In[65]:


# add clustering labels
community_venues_sorted.insert(0, 'Cluster Labels', kmeans.labels_)

SFV_merged = SFV_data

# merge LA_grouped with LA_data to add latitude/longitude for each neighborhood
SFV_merged = SFV_merged.join(community_venues_sorted.set_index('Community'), on='Community')


SFV_merged # check the last columns!


# In[66]:


SFV_merged.shape


# Verifying null values

# In[67]:


SFV_merged['Cluster Labels'].isnull().sum()


# Then, we removed the null value and verified it.

# In[68]:


SFV_merged=SFV_merged.dropna()


# In[69]:


SFV_merged['Cluster Labels'].isnull().sum()


# We must convert Cluster Labels type to an integer because it'll generate an error on Visualizing the results clusters--> TypeError: list indices must be integers or slices, not floats.

# In[70]:


SFV_merged.dtypes


# SFV_merged= SFV_merged['Cluster Labels'].astype(int)
# SFV_merged

# SFV_merged

# SFV_merged=SFV_merged['Cluster Labels'].astype(int)

# Finally, let's visualize the resulting clusters

# In[71]:


# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=10)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(SFV_merged['Latitude'], SFV_merged['Longitude'], SFV_merged['Community'], SFV_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster))
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        color=rainbow[cluster-1],
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# ## IV. Results

# ## 9. Examine Clusters: San Fernando Valley
# 
# To determine the discriminating venue categories that distinguish each cluster. Based on the defining categories, we assigned a name to each cluster.

# <h3>Cluster 1 </h3>

# In[72]:


# Cluster 1 ==> 'Cluster Labels'] == 0
# SFV_merged.columns[[4] ==> It is the column wanted to show-index[4]
cluster_1=SFV_merged.loc[SFV_merged['Cluster Labels'] == 0, SFV_merged.columns[[3] + list(range(5, SFV_merged.shape[1]))]]
cluster_1


# <h3>Cluster 2 </h3>

# In[73]:


# # Cluster 2 ==> 'Cluster Labels'] == 1
cluster_2=SFV_merged.loc[SFV_merged['Cluster Labels'] == 1, SFV_merged.columns[[3] + list(range(5, SFV_merged.shape[1]))]]
cluster_2


# <h3>Results : Most common Restaurants and Places to eat within Cluster 1 and 2 </h3> 

# <p>The type of food for the restaurant is not defined yet, either the location. Thus, it is early to suggest a definitive decision, although at this stage we have the information required, the different areas and the variety of Restaurants along the San Fernando Valley.</p>
# 
# The results of the most common venues help us to know more about the Restaurant industry and customer preferences. In our case, we focused on **Restaurants and Places to eat within both clusters**. The most common venues are International restaurants, such as Oriental, Italian, French, Middle East, Mediterranean, Mexican, and South American.

#  **Most common Restaurants and Places to eat within Cluster 1**

# In[74]:


#Source: https://thispointer.com/pandas-get-unique-values-in-single-or-multiple-columns-of-a-dataframe-in-python/
#uniqueValues = (empDfObj['Name'].append(empDfObj['Age'])).unique() 
# Get unique elements in multiple columns

uniqueValues = (cluster_1['1st Most Common Venue'].append(cluster_1['2nd Most Common Venue']).append(cluster_1['3rd Most Common Venue']).append(cluster_1['4th Most Common Venue']).append(cluster_1['5th Most Common Venue']).append(cluster_1['6th Most Common Venue']).append(cluster_1['7th Most Common Venue']).append(cluster_1['8th Most Common Venue']).append(cluster_1['9th Most Common Venue']).append(cluster_1['10th Most Common Venue'])).unique()

                                                                                                                                             
print('Unique elements in the 10 columns of Most Common Venues :')
print(uniqueValues)

#In case of required convert one-dimensional NumPy Array to List
#list1 = uniqueValues.tolist()
#print(f'List: {list1}')


# In[75]:


# processed by hand
Cluster1_most_common_venues_Restaurant_and_Places_in_SFV = ['Mexican Restaurant', 'Sandwich Place', 'Pizza Place', 'Food Truck',  'Vietnamese Restaurant', 'Sushi Restaurant', 'Chinese Restaurant', 'Indian Restaurant', 'Brazilian Restaurant', 'Fast Food Restaurant', 'American Restaurant','South American Restaurant','Japanese Restaurant', 'Middle Eastern Restaurant', 'Thai Restaurant', 'French Restaurant', 'Fried Chicken Joint', 'Mediterranean Restaurant', 'Salad Place', 'Filipino Restaurant', 'Diner', 'Italian Restaurant', 'Seafood Restaurant', 'Korean Restaurant', 'Taco Place', 'Greek Restaurant', 'Eastern European Restaurant', 'Cajun / Creole Restaurant', 'Shabu-Shabu Restaurant', 'Falafel Restaurant', 'Kosher Restaurant']
Cluster1_most_common_venues_Restaurant_and_Places_in_SFV


# <li>Cluster 1: along all the San Fernando Valley, the leader of the type of Restaurant is the Oriental, including Chinese, Japanese, Thai, Korean, etc. Follow by Mexican food, next, the Italian/ Pizza food. Finally, similar preference for Fast food restaurants, and Sandwich places.</li>     

# In[76]:


# processed by hand
Cluster1_most_commom_venues_top_5_restaurant = {'Italian_restaurant_and_Pizza_place': [16], 'Oriental_restaurant': [39], 'Mexican_Restaurant':[29], 'Fast Food':[12], 'Sandwich place':[12] }
Cluster1_most_commom_venues_top_5_restaurant


# In[77]:


plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    figsize=(11,5),
    values={'Italian_restaurant_and_Pizza_place':16, 'Oriental_restaurant':39, 'Mexican_Restaurant':29, 'Fast Food':12, 'Sandwich place':12},
    title={'label': 'Top 5 most common Restaurant and Places to eat of Cluster 1', 'fontdict': {'fontsize': 20}},
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1), 'fontsize': 12},
    plot_anchor='C')
plt.show


# **Most commom Restaurants and Places to eat in Cluster 2**

# <li>Cluster 2: Despite it is a small cluster,  yet there is a balanced tendency for Mediterranean food (Falafel), French restaurant, Food truck, and Filipino restaurant.</li> 

# In[78]:


# processed by hand
Cluster2_most_commom_venues_Restaurant_and_Places_in_SFV=['Falafel Restaurant','French Restaurant','Food Truck','Filipino Restaurant']
Cluster2_most_commom_venues_Restaurant_and_Places_in_SFV


# In[80]:


plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    figsize=(10,5),
    values={'Falafel Restaurant':1,'French Restaurant':1,'Food Truck':1,'Filipino Restaurant':1},
    title={'label': 'Top 4 most common Restaurant and Places to eat of Cluster 2', 'fontdict': {'fontsize': 20}},
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1), 'fontsize': 12},
    plot_anchor='C')
plt.show


# ## V.  Discussion

# According to the two above plots, there are distinct preferences for International cuisine. Hence, a similar kind of restaurant can be competitive in the San Fernando Valley. 
# <p>However, it would be better to know both criteria: the specific neighborhood where to set the restaurant and type of restaurant.</p>

# ## VI. Conclusion

# <p>The type of cuisine for the Restaurant is not defined yet. But, thanks to the clusters' finds, the client can decide his strategy, either competitive within the established market or innovative to different kinds of cuisines.</p>
# <p>Knowing the most common Restaurant and Places to eat helps to refine the options because the client can make wise decisions based on customers' preferences.</p> 

# # 10. Limitations

# The structured format of the data was difficult to reach, especially for the Boroughs.
# For this analysis, we researched and studied the geographic and administrative organization of Los Angeles county, concluding that the organization is not by boroughs. To simplify the selection, we dealt with two categories, our Target: San Fernando Valley, and, the Not target: =! San Fernando Valley. Hence, we reduced the colossus geography of Los Angeles County into 102 neighborhoods. Surpassing this issue, finally, we calculated the clusters in the San Fernando Valley.
# 
# It was not easy and took several attempts to get the unique values of the most common Restaurant and Places to eat by each cluster. Because we did not find a very efficient way to refine this search, the essential step we achieved by the append method, but in the end, we filtered by hand the small dataset.

# Autor: Francihelena Uzcategui
