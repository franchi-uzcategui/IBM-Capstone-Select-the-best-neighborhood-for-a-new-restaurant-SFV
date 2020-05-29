# Select-the-best-neighborhood-for-a-new-restaurant-SFV
 Capstone Project - The Battle of Neighborhoods (Week 1)

Business problem
A client is looking to open a casual restaurant in San Fernando Valley, California. The San Fernando Valley is an urbanized valley in Los Angeles County, California [1].
Nearly two-thirds of the Valley’s land area is part of the city of Los Angeles. The Valley as well called, is surrounded by many touristic and iconic places of Los Angeles city and Los Angeles county. For example, San Fernando Valley is 18 miles north of Downtown Los Angeles.
It is also about 17 miles from Santa Monica beach. These are just two of the numerous iconic’s locations close to the Valley.
Also, the entertainment industry’s headquartered are here, such a Disney, Warner Bros., Universal Studios, Dreamworks Animation, Cartoon Network, and Motion Picture Association of America. In the last years, doing business in the San Fernando Valley has been going flexibly. Its cities earned this reputation, being a stimulus to the economic growth of the region [2].
Thus, it is going to be promissory and prosper launch a new business here, in your case, a Restaurant.

Data
For this analysis, we require data of the borough, neighborhood, ZIP Code, longitude, and latitude. But, the county of Los Angeles does not have boroughs; it has unincorporated communities, incorporated cities, and neighborhoods of the city of Los Angeles – such as San Fernando Valley. Thus, to deal with the lack of boroughs, we defined two categories San Fernando Valley and Los Angeles.
To wrangle the data, we required to scrape the Wikipedia page and official pages, then cleaning it, joining between them, and creating a structured data frame.

Methodology
We explored the geographic coordinates and visualized the neighborhoods with Folium package.
We used the Foursquare API to explore the San Fernando Valley neighborhoods and segment them. Getting 181 unique categories of venues along the San Fernando Valley.
To segment all these venues is convenient to apply the K – means algorithm, because it finds common patterns and similar group venues within each neighborhood of San Fernando Valley. K-means to cluster the neighborhood into 2 clusters.

Results
Most common Restaurants and Places to eat within Cluster 1 and 2: The type of food for the restaurant is not defined yet, either the location. Thus, it is early to suggest a definitive decision, although at this stage we have the information required, the different areas and the variety of Restaurants along the San Fernando Valley.
The results of the most common venues help us to know more about the Restaurant industry and customer preferences. In our case, we focused on Restaurants and Places to eat within both clusters. The most common venues are International restaurants, such as Oriental, Italian, French, Middle East, Mediterranean, Mexican, and South American.

- Cluster 1: along all the San Fernando Valley, the leader of the type of Restaurant is the Oriental, including Chinese, Japanese, Thai, Korean, etc. Follow by Mexican food, next, the Italian/ Pizza food. Finally, similar preference for Fast food restaurants, and Sandwich places.
- Cluster 2: Despite it is a small cluster, yet there is a balanced tendency for Mediterranean food (Falafel), French restaurant, Food truck, and Filipino restaurant.

Conclusion
The type of cuisine for the Restaurant is not defined yet. But, thanks to the clusters’ finds, the client can decide his strategy, either competitive within the established market or innovative to different kinds of cuisines.
Knowing the most common Restaurant and Places to eat helps to refine the options because the client can make wise decisions based on customers’ preferences.
