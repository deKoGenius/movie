import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movie_data = pd.read_csv('./movie/movies.csv')
print(movie_data)
counter_vector = CountVectorizer(ngram_range=(1,3))
c_vector_genres = counter_vector.fit_transform(movie_data['genres'])

similarity_genre = cosine_similarity(c_vector_genres, c_vector_genres)
similarity_genre = pd.DataFrame(similarity_genre, index=movie_data['title'], columns=movie_data['title'])
# print(similarity_genre)

def get_content_based_collabor(title):
    return similarity_genre[title].sort_values(ascending=False)[:20]

# print(get_content_based_collabor('Toy Story (1995)'))
