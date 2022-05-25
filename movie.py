import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

rating_data = pd.read_csv('./movie/ratings.csv')
movie_data = pd.read_csv('./movie/movies.csv')

rating_data.drop('timestamp', axis=1, inplace=True)
# print(rating_data.head(2))

user_movie_data = pd.merge(rating_data, movie_data, on='movieId')

title_user = user_movie_data.pivot_table('rating', index='title', columns='userId')
title_user.fillna(0, inplace=True)
print(title_user)

item_based_collab = cosine_similarity(title_user)
# print(item_based_collab)
item_based_collab = pd.DataFrame(item_based_collab, index=title_user.index, columns=title_user.index)

# print(item_based_collab)

def get_item_based_collabor(title):
    return item_based_collab[title].sort_values(ascending=False)[:20]

print(get_item_based_collabor('Toy Story (1995)'))
