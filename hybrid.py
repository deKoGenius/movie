import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


title = 'Toy Story (1995)'
#read MovieLens data
rating_data = pd.read_csv('./movie/ratings.csv')
movie_data = pd.read_csv('./movie/movies.csv')

#set dataframe width and number of columns to display
desired_width=640
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

#delete unnecessary column
rating_data.drop('timestamp', axis=1, inplace=True)

#merge based on movieId
user_movie_data = pd.merge(rating_data, movie_data, on='movieId')

#create user-movie pivot table
title_user = user_movie_data.pivot_table('rating', index='title', columns='userId')
title_user.fillna(0, inplace=True)

#calculate cosine similarity of movie rating
item_based_collab = cosine_similarity(title_user)
item_based_collab = pd.DataFrame(item_based_collab, index=title_user.index, columns=title_user.index)
item_based_collab.sort_index(ascending=True)
item_based_collab.sort_index(axis=1, ascending=True)

#prepare a data table for content-based filtering
title_user.reset_index(inplace=True)
content_data= pd.merge(title_user, movie_data, on='title', how='inner')

#drop unnecessary columns
content_data.drop(content_data.iloc[:,1:672],axis=1, inplace=True)

# calculate cosine_similarity of genres
counter_vector = CountVectorizer(ngram_range=(1,3))
c_vector_genres = counter_vector.fit_transform(content_data['genres'])

similarity_genre = cosine_similarity(c_vector_genres, c_vector_genres)
similarity_genre = pd.DataFrame(similarity_genre, index=content_data['title'], columns=content_data['title'])

#calculate content-based and item-based module
original_data = pd.DataFrame(item_based_collab[title].sort_values(ascending=False)[1:101])
original_table=original_data.sort_values(by=title, ascending=False)[:5]
original_table=pd.merge(original_table, movie_data, on='title')
original_table.drop('movieId',axis=1,inplace=True)
print(original_table)
print('------------------------------------------------------')
reference_data = pd.DataFrame(similarity_genre[title])
for row in original_data.iterrows():
    original_data.loc[row[0].__str__()] = 0.8*row[1] + 0.2*reference_data.loc[row[0].__str__()]
re_table= original_data.sort_values(by=title, ascending=False)[:5]
re_table = pd.merge(re_table, movie_data, on='title')
re_table.drop('movieId',axis=1,inplace=True)
print(re_table)
# def get_content_based_collabor(title):
#     return similarity_genre[title].sort_values(ascending=False)[:20]

# def get_item_based_collabor(title):
#     return item_based_collab[title].sort_values(ascending=False)[:20]
# print(get_content_based_collabor('Toy Story (1995)'))
