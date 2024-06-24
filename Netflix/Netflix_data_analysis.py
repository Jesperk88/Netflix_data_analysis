import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read netflix data into python file
netflix_data = pd.read_csv('netflix_titles.csv')

# getting some information on the dataset
# print(netflix_data.head())
# for col in netflix_data.columns:
#     print(col)

# print(netflix_data.dtypes)
# print(netflix_data.info())
# print(netflix_data.shape)

# interested in release year, rating, genre(listed in), and country

# lets clean the data
# get rid of all duplicates
netflix_data.drop_duplicates(inplace = True)

# get rid of rows with no genre, rating, country, or release year
clean_data = netflix_data.dropna(subset=['country', 'release_year', 'rating', 'listed_in'])

# check if it worked
# print(clean_data.info())

# Question 1: For each year, what is the most published genre of a movie or show
# first lets remove rows without a genre or rating
genre_data = clean_data[['listed_in', 'release_year']].copy()
# now we split the genres in listed_in since it can be listed in multiple genres
genre_data['listed_in'] = genre_data['listed_in'].str.split(', ')
# This neat method 'explode' makes new rows so that an individual row that is listed in multiple genres is transferred to multiple rows covering all the genres one row at a time
genre_data = genre_data.explode('listed_in')
# now lets group by release_year and genre so we get combination of the both. Then to count them, we use a size method. Afterwards we reset the index for ease.
genre_data = genre_data.groupby(['release_year', 'listed_in']).size().reset_index(name = 'count')
# using loc we can return the rows which have a particular index label. By grouping by release year and using the method idxmax, it find the first instance of the maximum value of our combination of release year and genre and returns its index label.
genre_data = genre_data.loc[genre_data.groupby('release_year')['count'].idxmax()]
# to finish we sort and print
answerq1 = genre_data.sort_values(by = 'release_year')
print(answerq1)

# Continuation question 1: Say we are only interested in the past 15 years. Create a visualisation of how many movies or shows were release of the biggest genre for each year.
# first we filter the data to only contain data after 2007
answerq1['release_year'] = answerq1['release_year'].apply(lambda x: int(x))
vis = answerq1[answerq1['release_year'] >= 2007]

# we create a figure with a figsize big enough to contain each year
plt.figure(figsize=(15, 6))
# we now plot the count over each release year and add a marker for ease of seeing the visualisation
plt.plot(vis['release_year'], vis['count'], marker='o')
# to annotate which genre was most popular each year, we can use the annotate method. We use the iterrows method in order to iterate over the rows, and add a notation to them.
for index, row in vis.iterrows():
    plt.annotate(row['listed_in'], (row['release_year'], row['count']))
# let's also add labels, titles, and tickmarkers
plt.xlabel('Release Year')
plt.ylabel('Count')
plt.title('Most Published Genre by Year (2007 and later)')
plt.xticks(vis['release_year'])
plt.show()

# From this we can see that since 2012, so for the past 10 years, international movies genre has the most movies or shows released.

# Question 2: which director makes on average the longest movie?
# get rid of rows without director or duration
director_data = clean_data.dropna(subset=['director', 'duration'])
# for ease get rid of column i'm not interested in
director = director_data[['director', 'duration', 'type']].copy()
# filter the dataset on movies
director = director[director['type'] == 'Movie']
# applying a lambda function to split the duration string by the space, then taking the numbers, and converting to integer
director['duration'] = director['duration'].apply(lambda x: int(x.split(' ')[0]))
# creating a mean for each director's movie by grouping by director and taking the mean of duration for each
director = director.groupby('director')['duration'].mean()
# sorting the values to get the 10 directors with on average the longest movies
answerq2 = director.sort_values(ascending = False).head(10)
print(answerq2)


