import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the movie data and similarity matrix
def load_data():
    try:
        movies = pickle.load(open('movie_list.pkl', 'rb'))
        vectorizer = CountVectorizer(max_features=5000, stop_words='english')
        vector = vectorizer.fit_transform(movies['tags']).toarray()
        similarity = cosine_similarity(vector)
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Function to recommend movies
def recommend(movie, movies, similarity):
    if movie not in movies['title'].values:
        return ["Movie not found!"]
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Streamlit UI
st.title('Movie Recommendation System')

# Load data
movies, similarity = load_data()

if movies is not None and similarity is not None:
    # User interaction
    movie_list = movies['title'].values
    selected_movie = st.selectbox('Select a movie:', movie_list)

    if st.button('Recommend'):
        recommendations = recommend(selected_movie, movies, similarity)
        if recommendations[0] == "Movie not found!":
            st.write(recommendations[0])
        else:
            st.write('Recommended Movies:')
            for movie in recommendations:
                st.write(movie)
else:
    st.write("Failed to load movie data.")
