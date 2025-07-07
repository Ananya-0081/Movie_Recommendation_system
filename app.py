import pickle
import pandas as pd
import streamlit as stimport requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Movie Recommender", layout="wide")


# --- Inject Netflix-style Dark Theme ---
def local_css():
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #141414;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }

            h1, h2, h3, h4, h5, h6 {
                color: #e50914;
                font-weight: 700;
                margin-bottom: 1rem;
            }

            /* Selectbox Label */
            .stSelectbox > label {
                color: #ffffff !important;
                font-weight: 500;
                font-size: 1.1rem;
            }

            /* Selectbox Dropdown */
            .stSelectbox div[data-baseweb="select"] {
                background-color: #1f1f1f;
                color: white;
                border: 1px solid #333;
                border-radius: 6px;
            }

            /* Button */
            .stButton>button {
                background-color: #e50914;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 1rem;
                font-weight: bold;
                border-radius: 5px;
                transition: all 0.3s ease;
            }

            .stButton>button:hover {
                background-color: #f40612;
                transform: scale(1.02);
            }

            /* Text, Captions */
            .stCaption, .stText, .stMarkdown {
                color: #dddddd !important;
                font-size: 0.95rem;
                text-align: center;
            }

            /* Image Styling */
            img {
                border-radius: 12px;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
            }

            /* Optional override for common Streamlit auto-generated classes */
            [class^="css-"] {
                color: #ffffff;
            }
        </style>
    """, unsafe_allow_html=True)




local_css()

# --- API Setup ---
API_KEY = st.secrets["tmdb"]["api_key"]

# --- Setup Retry Logic for API ---
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)


# --- Fetch Poster from TMDb ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (MovieRecommender/1.0)"
    }
    try:
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        st.warning(f"Poster fetch failed for movie ID {movie_id}: {e}")

    return "https://via.placeholder.com/300x450?text=No+Poster"


# --- Recommend Similar Movies ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_titles = []
    recommended_posters = []
    for item in distances[1:7]:
        movie_id = movies.iloc[item[0]].movie_id
        recommended_titles.append(movies.iloc[item[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.5)
    return recommended_titles, recommended_posters


# --- UI Content ---
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# --- Load Data ---
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- User Input ---
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie:", movie_list)

# --- Recommend Button ---
if st.button('🔍 Recommend'):
    titles, posters = recommend(selected_movie)
    cols = st.columns(len(titles))
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx])
            st.caption(f"🎞 {titles[idx]}")
