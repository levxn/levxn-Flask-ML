# import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

# load the movie dataset
movies = pd.read_csv("static/main_data.csv")

# create a CountVectorizer object
cv = CountVectorizer()

# apply the CountVectorizer object to the 'genres' column
count_matrix = cv.fit_transform(movies['genres'])

# apply TruncatedSVD to reduce the dimensionality of the count matrix
svd = TruncatedSVD(n_components=10)
count_matrix = svd.fit_transform(count_matrix)

# calculate the cosine similarity of the reduced count matrix
cosine_sim = cosine_similarity(count_matrix)

# define a function to get recommendations based on user input


def get_recommendations(user_genre, cosine_sim=cosine_sim, movies=movies, count_matrix=count_matrix, svd=svd):
    genre_movies = movies[movies['genres'].str.contains(user_genre)]
    title = genre_movies['title'].iloc[1]
    # create a list of indices for movie titles
    indices = pd.Series(movies.index, index=movies['title'])

    # find the index of the movie that matches the user input
    idx = indices[title]

    # transform the user input using the same CountVectorizer object and TruncatedSVD instance
    input_vec = cv.transform([movies.loc[idx, 'genres']])
    input_vec = svd.transform(input_vec)

    sim_scores = list(enumerate(cosine_sim[input_vec.flatten().astype(int)]))

    # sort the movies based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1].all(), reverse=True)

    # get the movie indices
    movie_indices = [i for i, x in enumerate(
        sim_scores) if x[0] in genre_movies.index]

    # return the top 10 most similar movies
    return movies['title'].iloc[movie_indices]


if __name__ == '__main__':
    # get user input for genre
    user_genre = input("Enter your favorite genre: ")
    user_genre = user_genre.capitalize()

    # filter movies by user genre input

    # get recommendations based on user input
    recommendations = get_recommendations(user_genre)

    # print the recommendations
    print("Recommended movies based on your genre choice: ")
    print(recommendations)
