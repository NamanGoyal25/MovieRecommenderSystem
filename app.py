# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()  # Add this near the top of your script
#
#
# # Modified part of your code
# def fetch_poster(movie_id):
#     api_key = None
#     try:
#         pass
#         api_key = st.secrets["TMDB_API_KEY"]  # Prioritize Streamlit secrets
#     except KeyError:
#         api_key = os.getenv("TMDB_API_KEY")  # Fallback to .env
#         if not api_key:
#             st.error("TMDB API key not found. Please configure it in .streamlit/secrets.toml or .env.")
#             return None
#
#     try:
#         response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
#         response.raise_for_status()  # Raise an error for bad responses
#         data = response.json()
#         if 'poster_path' in data:
#             return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#         else:
#             st.warning(f"No poster found for movie ID {movie_id}")
#             return None
#     except requests.RequestException as e:
#         st.error(f"Error fetching poster for movie ID {movie_id}: {e}")
#         return None
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#         recommended_movie_posters.append(fetch_poster(movie_id))
#     return recommended_movie_names, recommended_movie_posters
#
#
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# # similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# import streamlit as st
# import pickle
# import requests
# import os
#
# @st.cache_data
# def download_similarity_pkl():
#     url = "https://drive.google.com/uc?export=download&id=17SKEed3Ed5dJHnkaBW-izCHJESnnxgLI"
#     local_path = "similarity.pkl"
#     if not os.path.exists(local_path):
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error if the download fails
#         with open(local_path, 'wb') as f:
#             f.write(response.content)
#     return local_path
#
# # Load similarity matrix
# similarity_path = download_similarity_pkl()
# similarity = pickle.load(open(similarity_path, 'rb'))
#
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     'Which movie do you like?',
#     movies['title'].values)
#
# if st.button('Recommend'):
#     recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])
#


import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv


# Load environment variables from .env file if it exists
load_dotenv()


def fetch_poster(movie_id):
    # First try to get API key from Streamlit secrets (for cloud deployment)
    api_key = None

    # If still no API key, use the hardcoded one as last resort
    if not api_key:
        api_key = "445a186720c0bc93aba3895bfe64ac69"  # This should be removed in production
        # st.warning("Using default API key. Please set up your own API key for better reliability.")

    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            # Return a placeholder image URL if no poster is available
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"


def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movie_names = []
        recommended_movie_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_names.append(movies.iloc[i[0]].title)
            poster = fetch_poster(movie_id)
            recommended_movie_posters.append(poster)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        # Return empty lists or placeholder data in case of error
        return ["Error loading recommendations"] * 5, ["https://via.placeholder.com/500x750?text=Error"] * 5


# App title and description
st.title('Movie Recommender System')
st.write('Select a movie you like and get recommendations for similar movies!')


# Load movie data
@st.cache_data
def load_movies():
    try:
        movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        return pd.DataFrame(movies_dict)
    except Exception as e:
        st.error(f"Error loading movie data: {e}")
        return pd.DataFrame(columns=['title', 'movie_id'])


# Load similarity matrix
@st.cache_data
def load_similarity():
    try:
        # First try to load locally
        if os.path.exists('similarity.pkl'):
            return pickle.load(open('similarity.pkl', 'rb'))
        else:
            # If not available locally, download from Google Drive
            st.info("Downloading similarity matrix... This may take a moment.")
            url = "https://drive.google.com/uc?export=download&id=17SKEed3Ed5dJHnkaBW-izCHJESnnxgLI"
            response = requests.get(url)
            response.raise_for_status()
            with open('similarity.pkl', 'wb') as f:
                f.write(response.content)
            return pickle.load(open('similarity.pkl', 'rb'))
    except Exception as e:
        st.error(f"Error loading similarity data: {e}")
        # Return an empty matrix in case of error
        import numpy as np
        return np.array([])


# Load data
with st.spinner('Loading movie data...'):
    movies = load_movies()

with st.spinner('Loading recommendation engine...'):
    similarity = load_similarity()

# Movie selection
if not movies.empty:
    selected_movie_name = st.selectbox(
        'Which movie do you like?',
        movies['title'].values
    )

    # Recommendation button
    if st.button('Recommend'):
        with st.spinner('Finding recommendations...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

            # Display recommendations in columns
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])
else:
    st.error("Unable to load movie data. Please check the application logs.")